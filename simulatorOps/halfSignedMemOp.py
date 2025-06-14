
import struct
import simulatorOps.utils as utils
from simulatorOps.abstractOp import AbstractOp, ExecutionException

from stateManager import StateManager
appState = StateManager()

class HalfSignedMemOp(AbstractOp):
    saveStateKeys = frozenset(("condition", 
                                "imm", "pre", "sign", "byte", "writeback", "mode", "signed",
                                "basereg", "rd", "offsetImm", "offsetReg"))

    def __init__(self):
        super().__init__()
        self._type = utils.InstrType.memop

    def decode(self):
        instrInt = self.instrInt
        if not (utils.checkMask(instrInt, (7, 4), (27, 26, 25))):
            raise ExecutionException(appState.getT(10),
                                        internalError=False)

        # Retrieve the condition field
        self._decodeCondition()

        # This is the inverse of LDR/STR, if bit 22 is set, then offset IS an immediate value
        self.imm = bool(instrInt & (1 << 22))   
        self.pre = bool(instrInt & (1 << 24))
        self.sign = 1 if instrInt & (1 << 23) else -1
        self.byte = not bool(instrInt & (1 << 5))
        self.signed = bool(instrInt & (1 << 6))
        # See 4.9.1 (with post, writeback is redundant and always implicitely on)
        self.writeback = bool(instrInt & (1 << 21)) or not self.pre
        self.mode = "LDR" if instrInt & (1 << 20) else "STR"

        self.basereg = (instrInt >> 16) & 0xF
        self.rd = (instrInt >> 12) & 0xF

        if self.imm:
            # The immediate offset is divided in 2 nibbles:
            # the 4 LSB are at positions [3, 2, 1, 0]
            # the 4 MSB are at positions [11, 10, 9, 8]
            self.offsetImm = instrInt & 0xF + ((instrInt >> 4) & 0xF0)
        else:
            # No shift allowed with these instructions
            self.offsetReg = instrInt & 0xF


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
            regDesc = utils.regSuffixWithBank(self.offsetReg, bank)
            if self.sign > 0:
                descoffset = appState.getT(4).format(regDesc)
            else:
                descoffset = appState.getT(5).format(regDesc)

            addr += self.sign * simulatorContext.regs[self.offsetReg]
            self._readregs |= utils.registerWithCurrentBank(self.offsetReg, bank)

        realAddr = addr if self.pre else baseval
        sizeaccess = 1 if self.byte else 2
        sizedesc = "1 octet" if sizeaccess == 1 else "{} octets".format(sizeaccess)

        disassembly += "S" if self.signed else ""
        disassembly += "B" if sizeaccess == 1 else "H" if sizeaccess == 2 else ""
        disassembly += " R{}, [R{}".format(self.rd, self.basereg)

        if self.mode == 'LDR':
            if self.pre:
                description += descoffset
                description += appState.getT(6).format(sizedesc, utils.regSuffixWithBank(self.rd, bank))
            else:
                description += appState.getT(7).format(sizedesc, utils.regSuffixWithBank(self.rd, bank))
                description += descoffset
            
            if self.signed:
                description += appState.getT(8).format(7 if self.byte else 15, 8 if self.byte else 16)
            
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
                        res = struct.unpack("<B" if self.byte else "<H", m)[0]
                        self._nextInstrAddr = res

        else:       # STR
            descRange = appState.getT(9) if self.byte else appState.getT(10)
            if self.pre:
                description += descoffset
                description += appState.getT(11) + descRange + appState.getT(12).format(utils.regSuffixWithBank(self.rd, bank), sizedesc)
            else:
                description += appState.getT(13) + descRange + appState.getT(14).format(utils.regSuffixWithBank(self.rd, bank), sizedesc)
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
                disassembly += ", R{}".format(self.offsetReg) + "]"
        else:
            # Post (a post-incrementation of 0 is useless)
            disassembly += "]"
            if self.imm and self.offsetImm != 0:
                disassembly += ", #{}".format(hex(self.sign * self.offsetImm))
            elif not self.imm:
                disassembly += ", R{}".format(self.offsetReg)
        #else:
            # Weird case, would happen if we combine post-incrementation and immediate offset of 0
        #    disassembly += "]"

        if self.writeback:
            self._writeregs |= utils.registerWithCurrentBank(self.basereg, bank)
            description += appState.getT(15).format(utils.regSuffixWithBank(self.basereg, bank))
            if self.pre:
                disassembly += "!"

        description += "</ol>"

        simulatorContext.regs.reactivateBreakpoints()
        return disassembly, description
    

    def execute(self, simulatorContext):
        if not self._checkCondition(simulatorContext.regs):
            # Nothing to do, instruction not executed
            self.countExecConditionFalse += 1
            return
        self.countExec += 1

        addr = baseval = simulatorContext.regs[self.basereg]
        if self.imm:
            addr += self.sign * self.offsetImm
        else:
            addr += self.sign * simulatorContext.regs[self.offsetReg]

        realAddr = addr if self.pre else baseval
        s = 1 if self.byte else 2
        if self.mode == 'LDR':
            m = simulatorContext.mem.get(realAddr, size=s)
            if m is None:       # No such address in the mapped memory, we cannot continue
                raise ExecutionException(appState.getT(16).format(s, realAddr))
            res = struct.unpack("<B" if self.byte else "<H", m)[0]

            simulatorContext.regs[self.rd] = res
            if self.signed:
                simulatorContext.regs[self.rd] |= 0xFFFFFF00 * ((res >> 7) & 1) if self.byte else 0xFFFF0000 * ((res >> 15) & 1)
                
            if self.rd == simulatorContext.PC:
                self.pcmodified = True
        else:       # STR
            valWrite = simulatorContext.regs[self.rd]
            if self.rd == simulatorContext.PC and simulatorContext.PCSpecialBehavior:
                valWrite += 4       # Special case for PC (see ARM datasheet, 4.9.4)
            valWrite &= 0xFFFF
            simulatorContext.mem.set(realAddr, valWrite, size=1 if self.byte else 2)

        if self.writeback:
            simulatorContext.regs[self.basereg] = addr
