import simulatorOps.utils as utils
from simulatorOps.abstractOp import AbstractOp, ExecutionException

from stateManager import StateManager
appState = StateManager()

class SoftInterruptOp(AbstractOp):
    saveStateKeys = frozenset(("condition", "datauser"))

    def __init__(self):
        super().__init__()
        self._type = utils.InstrType.softinterrupt

    def decode(self):
        instrInt = self.instrInt
        if not (utils.checkMask(instrInt, (24, 25, 26, 27), ())):
            raise ExecutionException(appState.getT(0),
                                        internalError=False)

        # Retrieve the condition field
        self._decodeCondition()
        self.datauser = instrInt & 0xFFFFFF

    def explain(self, simulatorContext):
        self.resetAccessStates()
        bank = simulatorContext.regs.mode
        simulatorContext.regs.deactivateBreakpoints()
        
        description = "<ol>\n"
        disCond, descCond = self._explainCondition()
        description += descCond
        description += appState.getT(1)
        description += appState.getT(2)
        description += appState.getT(3)
        description += appState.getT(4)
        disassembly = "SVC{} 0x{:X}".format(disCond, self.datauser)
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

        keepPC = simulatorContext.regs[15]
        # We enter a software interrupt
        keepCPSR = simulatorContext.regs.CPSR
        simulatorContext.regs.mode = "SVC"                  # Set the register bank
        simulatorContext.regs.SPSR = keepCPSR               # Save the CPSR in the current SPSR
        # Does entering SVC interrupt deactivate IRQ and/or FIQ?
        simulatorContext.regs[14] = keepPC
        simulatorContext.regs[15] = 0x08                    # Entrypoint for the SVC
        self.pcmodified = True

        if keepPC - simulatorContext.pcoffset in simulatorContext.assertionCkpts and \
            simulatorContext.assertionData[keepPC - simulatorContext.pcoffset][0][0] != "BEFORE":
            # There is an assertion after the SVC call, user probably wanted this to be
            # executed when the interrupt returns
            # We use the same mechanism than with assertion with BL
            key = keepPC - simulatorContext.pcoffset + 4
            assertionInfo = []
            for ad in simulatorContext.assertionData[keepPC - simulatorContext.pcoffset]:
                assertionInfo.append(("BEFORE", ad[1], ad[2]))
            if key in simulatorContext.assertionData:
                for ad in simulatorContext.assertionData[key]:
                    # We don't want to insert it more than one time
                    if ad[0] == "BEFORE":
                        break
                else:
                    simulatorContext.assertionData[key].extend(assertionInfo)
            else:
                simulatorContext.assertionData[key] = assertionInfo
                simulatorContext.assertionCkpts.add(key)