import struct
import simulatorOps.utils as utils
from simulatorOps.abstractOp import AbstractOp, ExecutionException

from stateManager import StateManager
appState = StateManager()

class MemOp(AbstractOp):
    saveStateKeys = frozenset(("condition", 
                                "imm", "pre", "sign", "byte", "writeback", "mode", "nonprivileged",
                                "basereg", "rd", "offsetImm", "offsetReg", "offsetRegShift"))

    def __init__(self):
        super().__init__()
        self._type = utils.InstrType.memop

    def decode(self):
        instrInt = self.instrInt
        if not (utils.checkMask(self.instrInt, (26, 25), (4, 27)) or utils.checkMask(self.instrInt, (26,), (25, 27))):
            raise ExecutionException(appState.getT(0),
                                        internalError=False)

        # Retrieve the condition field
        self._decodeCondition()

        # For LDR/STR, imm is 0 if offset IS an immediate value (4-26 datasheet)
        self.imm = not bool(instrInt & (1 << 25))   
        self.pre = bool(instrInt & (1 << 24))
        self.sign = 1 if instrInt & (1 << 23) else -1
        self.byte = bool(instrInt & (1 << 22))
        # See 4.9.1 (with post, writeback is redundant and always on)
        self.writeback = bool(instrInt & (1 << 21)) or not self.pre
        # See same section, with post-inc, writeback is actually used to indicate an LDRT instruction
        self.nonprivileged = bool(instrInt & (1 << 21)) and not self.pre
        self.mode = "LDR" if instrInt & (1 << 20) else "STR"

        self.basereg = (instrInt >> 16) & 0xF
        self.rd = (instrInt >> 12) & 0xF
        if self.imm:
            self.offsetImm = instrInt & 0xFFF
        else:
            self.offsetReg = instrInt & 0xF
            # Cannot be a register shift
            self.offsetRegShift = utils.shiftInfo(type=utils.shiftMappingR[(instrInt >> 5) & 0x3],
                                                    immediate=True,
                                                    value=(instrInt >> 7) & 0x1F)


    def explain(self, simulatorContext):
        self.resetAccessStates()
        bank = simulatorContext.regs.mode
        simulatorContext.regs.deactivateBreakpoints()
        
        disassembly = self.mode
        description = "<ol>\n"
        disCond, descCond = self._explainCondition()
        description += descCond
        disassembly += disCond

        self._readregs = utils.registerWithCurrentBank(self.basereg, bank)
        addr = baseval = simulatorContext.regs[self.basereg]

        description += appState.getT(1).format(utils.regSuffixWithBank(self.basereg, bank))
        descoffset = ""
        if self.imm:
            addr += self.sign * self.offsetImm
            if self.offsetImm > 0:
                if self.sign > 0:
                    descoffset = appState.getT(2).format(self.offsetImm)
                else:
                    descoffset = appState.getT(3).format(self.offsetImm)
        else:
            shiftDesc = utils.shiftToDescription(self.offsetRegShift, bank)
            regDesc = utils.regSuffixWithBank(self.offsetReg, bank)
            if self.sign > 0:
                descoffset = appState.getT(4).format(regDesc, shiftDesc)
            else:
                descoffset = appState.getT(5).format(regDesc, shiftDesc)

            _, sval = utils.applyShift(simulatorContext.regs[self.offsetReg], self.offsetRegShift, simulatorContext.regs.C)
            addr += self.sign * sval
            self._readregs |= utils.registerWithCurrentBank(self.offsetReg, bank)

        realAddr = addr if self.pre else baseval
        sizeaccess = 1 if self.byte else 4
        sizedesc = appState.getT(6) if sizeaccess == 1 else appState.getT(7).format(sizeaccess)

        disassembly += "B" if sizeaccess == 1 else ""
        if self.nonprivileged:
            disassembly += "T"
        disassembly += " R{}, [R{}".format(self.rd, self.basereg)

        if self.mode == 'LDR':
            if self.pre:
                description += descoffset
                description += appState.getT(8).format(sizedesc, utils.regSuffixWithBank(self.rd, bank))
            else:
                description += appState.getT(9).format(sizedesc, utils.regSuffixWithBank(self.rd, bank))
                description += descoffset
            
            self._readmem = set(range(realAddr, realAddr+sizeaccess))
            self._writeregs |= utils.registerWithCurrentBank(self.rd, bank)

            if self.rd == simulatorContext.PC:
                try:
                    m = simulatorContext.mem.get(realAddr, size=sizeaccess, mayTriggerBkpt=False)
                except ExecutionException as ex:
                    # We do not want to handle user errors here;
                    # If there is an issue with the memory access, we simply carry on
                    pass
                else:
                    if m is not None:
                        res = struct.unpack("<B" if self.byte else "<I", m)[0]
                        self._nextInstrAddr = res

        else:       # STR
            if self.pre:
                description += descoffset
                description += appState.getT(10).format(utils.regSuffixWithBank(self.rd, bank), sizedesc)
            else:
                description += appState.getT(11).format(utils.regSuffixWithBank(self.rd, bank), sizedesc)
                description += descoffset

            self._writemem = set(range(realAddr, realAddr+sizeaccess))
            self._readregs |= utils.registerWithCurrentBank(self.rd, bank)

        if self.pre:
            if self.imm:
                if self.offsetImm == 0:
                    disassembly += "]"
                else:
                    disassembly += ", #{}]".format(hex(self.sign * self.offsetImm))
            else:
                disassembly += ", R{}".format(self.offsetReg)
                disassembly += utils.shiftToInstruction(self.offsetRegShift) + "]"
        else:
            # Post (a post-incrementation of 0 is useless)
            disassembly += "]"
            if self.imm and self.offsetImm != 0:
                disassembly += ", #{}".format(hex(self.sign * self.offsetImm))
            elif not self.imm:
                disassembly += ", R{}".format(self.offsetReg)
                disassembly += utils.shiftToInstruction(self.offsetRegShift)

        if self.writeback:
            self._writeregs |= utils.registerWithCurrentBank(self.basereg, bank)
            description += appState.getT(12).format(utils.regSuffixWithBank(self.basereg, bank))
            if self.pre:
                disassembly += "!"

        description += "</ol>"

        simulatorContext.regs.reactivateBreakpoints()
        return disassembly, description
    

    def execute(self, simulatorContext):
        self.pcmodified = False
        if not self._checkCondition(simulatorContext.regs):
            # Nothing to do, instruction not executed
            self.countExecConditionFalse += 1
            return
        self.countExec += 1

        addr = baseval = simulatorContext.regs[self.basereg]
        if self.imm:
            addr += self.sign * self.offsetImm
        else:
            _, sval = utils.applyShift(simulatorContext.regs[self.offsetReg], self.offsetRegShift, simulatorContext.regs.C)
            addr += self.sign * sval

        realAddr = addr if self.pre else baseval
        s = 1 if self.byte else 4
        if self.mode == 'LDR':
            m = simulatorContext.mem.get(realAddr, size=s)
            if m is None:       # No such address in the mapped memory, we cannot continue
                raise ExecutionException(appState.getT(13).format(s, realAddr))
            res = struct.unpack("<B" if self.byte else "<I", m)[0]

            simulatorContext.regs[self.rd] = res
            if self.rd == simulatorContext.PC:
                self.pcmodified = True
        else:       # STR
            valWrite = simulatorContext.regs[self.rd]
            if self.rd == simulatorContext.PC and simulatorContext.PCSpecialBehavior:
                valWrite += 4       # Special case for PC (see ARM datasheet, 4.9.4)
            simulatorContext.mem.set(realAddr, valWrite, size=1 if self.byte else 4)

        if self.writeback:
            simulatorContext.regs[self.basereg] = addr
