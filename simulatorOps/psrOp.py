import simulatorOps.utils as utils
from simulatorOps.abstractOp import AbstractOp, ExecutionException

from stateManager import StateManager
appState = StateManager()

class PSROp(AbstractOp):
    saveStateKeys = frozenset(("condition", 
                                "usespsr", "modeWrite", "flagsOnly", "imm",
                                "rd", "val", "shift", "opcode"))

    def __init__(self):
        super().__init__()
        self._type = utils.InstrType.psrtransfer

    def decode(self):
        instrInt = self.instrInt
        # This one is tricky
        # The signature looks like a data processing operation, BUT
        # it sets the "opcode" to an operation beginning with 10**, 
        # and the only operations that match this are TST, TEQ, CMP and CMN
        # It is said that for these ops, the S flag MUST be set to 1
        # With MSR and MRS, the bit representing the S flag is always 0, 
        # so we can differentiate these instructions...
        if not (utils.checkMask(instrInt, (19, 24), (27, 26, 23, 20))):
            raise ExecutionException(appState.getT(0),
                                        internalError=False)

        # Retrieve the condition field
        self._decodeCondition()

        self.usespsr = bool(instrInt & (1 << 22))
        self.modeWrite = bool(instrInt & (1 << 21))
        self.flagsOnly = not bool(instrInt & (1 << 16))
        self.imm = bool(instrInt & (1 << 25))
        self.rd = (instrInt >> 12) & 0xF

        if self.imm and self.flagsOnly:       # Immediate mode is allowed only for flags-only mode
            self.val = instrInt & 0xFF
            self.shift = utils.shiftInfo(type="ROR",
                                            immediate=True,
                                            value=((instrInt >> 8) & 0xF)*2)    # see 4.5.3 of ARM doc to understand the * 2   
        else:
            self.val = instrInt & 0xF
            self.shift = utils.shiftInfo(type="ROR",
                                            immediate=True,
                                            value=0)       # No rotate with registers for these particular instructions
        
        self.opcode = "MSR" if self.modeWrite else "MRS"

    def explain(self, simulatorContext):
        self.resetAccessStates()
        bank = simulatorContext.regs.mode
        simulatorContext.regs.deactivateBreakpoints()
        
        disassembly = self.opcode
        description = "<ol>\n"
        disCond, descCond = self._explainCondition()
        description += descCond

        disassembly += disCond
        if self.modeWrite:
            disassembly += " SPSR" if self.usespsr else " CPSR"
            if self.flagsOnly:
                disassembly += "_flg"
                if self.imm:
                    _unused, valToSet = utils.applyShift(self.val, self.shift, simulatorContext.regs.C)
                    description += appState.getT(1).format(valToSet, "SPSR" if self.usespsr else "CPSR")
                    disassembly += ", #{}".format(hex(valToSet))
                else:
                    disassembly += ", R{}".format(self.val)
                    self._writeregs |= utils.registerWithCurrentBank(self.val, bank)
                    description += appState.getT(2).format(utils.regSuffixWithBank(self.val, bank))
                    description += appState.getT(3).format("SPSR" if self.usespsr else "CPSR")
            else:
                description += appState.getT(4).format(utils.regSuffixWithBank(self.val, bank))
                description += appState.getT(5).format("SPSR" if self.usespsr else "CPSR")
                disassembly += ", R{}".format(self.val)
        else:       # Read
            disassembly += " R{}, {}".format(self.rd, "SPSR" if self.usespsr else "CPSR")
            self._writeregs |= utils.registerWithCurrentBank(self.rd, bank)
            description += appState.getT(6).format("SPSR" if self.usespsr else "CPSR")
            description += appState.getT(7).format(utils.regSuffixWithBank(self.rd, bank))

        description += "</ol>"
        simulatorContext.regs.reactivateBreakpoints()
        return disassembly, description
    
    def execute(self, simulatorContext):
        if not self._checkCondition(simulatorContext.regs):
            # Nothing to do, instruction not executed
            self.countExecConditionFalse += 1
            return
        self.countExec += 1

        if self.modeWrite:
            if self.usespsr and simulatorContext.regs.mode == "User":
                # Check if SPSR exists (we are not in user mode)
                raise ExecutionException(appState.getT(8))
            if self.flagsOnly:
                if self.imm:
                    valToSet = self.val
                    if self.shift[2] != 0:
                        _unused, valToSet = utils.applyShift(valToSet, self.shift, simulatorContext.regs.C)
                else:
                    valToSet = simulatorContext.regs[self.val] & 0xF0000000   # We only keep the condition flag bits
                if self.usespsr:
                    valToSet |= simulatorContext.regs.SPSR & 0x0FFFFFFF
                else:
                    valToSet |= simulatorContext.regs.CPSR & 0x0FFFFFFF
            else:
                valToSet = simulatorContext.regs[self.val]

            if (valToSet & 0x1F) not in simulatorContext.regs.bits2mode:
                raise ExecutionException(appState.getT(9).format(valToSet & 0x1F, "SPSR" if self.usespsr else "CPSR"))

            if self.usespsr:
                simulatorContext.regs.SPSR = valToSet
            else:
                if not simulatorContext.allowSwitchModeInUserMode and simulatorContext.regs.mode == "User" and simulatorContext.regs.CPSR & 0x1F != valToSet & 0x1F:
                    raise ExecutionException(appState.getT(10))
                simulatorContext.regs.CPSR = valToSet
        else:       # Read
            if self.usespsr and simulatorContext.regs.mode == "User":
                # Check if SPSR exists (we are not in user mode)
                raise ExecutionException(appState.getT(11))
            else:
                simulatorContext.regs[self.rd] = simulatorContext.regs.SPSR if self.usespsr else simulatorContext.regs.CPSR
