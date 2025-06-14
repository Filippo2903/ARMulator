import struct
from collections import defaultdict

from ply.lex import LexError
from tokenizer import ParserError, lexer
import yaccparser
from settings import getSetting

from stateManager import StateManager
appState = StateManager()

"""
    @private
"""
memory_configs = {
    "simulation": {"INTVEC": 0x00, "CODE": 0x80, "DATA": 0x1000},
    "test": {"INTVEC": 0x100000, "CODE": 0x100080, "DATA": 0x101000},
}


class AssemblerError(Exception):
    """
    @private
    """

    def __init__(self, msg):
        super().__init__(msg)


class ParsingError(AssemblerError):
    """
    @private
    """

    def __init__(self, msg):
        super().__init__(msg)


class RangeError(AssemblerError):
    """
    @private
    """

    def __init__(self, msg):
        super().__init__(msg)


class ParseError:
    """
    @private
    """

    dictErrors = {
        "SYNTAX": appState.getT(0),
        "RANGE": appState.getT(1),
        "INVINSTR": appState.getT(2),
    }

    def __init__(self, etype, msg, gravity="ERROR"):
        self.t = etype
        self.m = msg
        self.gravity = gravity

    def __str__(self):
        return "{} : {}".format(self.t, self.m)


def parse(code, memLayout="simulation"):
    """
    Parse and compile ARM assembly code.
    :param code: a string containing ARM assembly
    :param memLayout: a string indicating the memory layout wanted.
                    "simulation" is a standard memory layout for simulation,
                        with code section beginning at 0x80 (not too far from the interrupt vector)
                    "test" is a memory layout compliant with QEMU needs,
                        so that epater can be tested against it
    :return: A tuple containing :
     1) a bytes object (the generated bytecode)
     2) a list object which maps each address in the bytecode to a line in the
        provided ARM assembly
     3) an error object which is an empty list if there is not error, else a 3-tuple:
         A) a string indicating where we want to write the error,
            either "error" (top display) or "codeerror" (in the code)
         B) if "error", description of the error
            if "codeerror", integer of the line of error
         C) if "codeerror", description of the error

    """

    listErrors = []
    if getSetting("PCbehavior") == "real":
        raise NotImplementedError(appState.getT(3))
    pcoffset = 8 if getSetting("PCbehavior") == "+8" else 0

    # First pass : the input code is passed through the lexer and the parser
    # Each line is parsed independently
    # The parser always returns a dictionnary
    addrToLine = defaultdict(list)
    currentAddr, currentSection = -1, None
    labelsAddr = {}
    requiredLabelsPtr = []
    maxAddrBySection = {
        "INTVEC": memory_configs[memLayout]["INTVEC"],
        "CODE": memory_configs[memLayout]["CODE"],
        "DATA": memory_configs[memLayout]["DATA"],
    }
    snippetMode = False
    # We add a special field in the bytecode info to tell the simulator the start address of each section
    bytecode = {
        "__MEMINFOSTART": {"SNIPPET_DUMMY_SECTION": 0},
        "__MEMINFOEND": {"SNIPPET_DUMMY_SECTION": 0},
    }
    unresolvedDepencencies = {}
    assertions = defaultdict(list)
    lastLineType = None
    totalMemAllocated = 0
    emptyLines = set()
    lineToAddr = {}
    viewedSections = set()
    for i, line in enumerate(code):
        line = line.strip()
        if ";" in line:
            # Remove the comments
            line = line[: line.find(";")]
        if len(line) == 0:
            # Empty line
            emptyLines.add(i)
            continue

        line += "\n"
        try:
            # We ensure that we are in the initial state of the lexer (in case of error in the previous lines)
            lexer.begin("INITIAL")
            parsedLine = yaccparser.parser.parse(input=line)
        except LexError as e:
            listErrors.append(("codeerror", i, appState.getT(4)))
            continue
        except ParserError as e:
            listErrors.append(("codeerror", i, str(e)))
            continue
        except Exception as e:
            listErrors.append(
                ("codeerror", i, appState.getT(5))
            )
            print(str(e))
            continue
        else:
            if parsedLine is None or len(parsedLine) == 0:
                # Unknown error, but the instruction did not parse
                listErrors.append(("codeerror", i, appState.getT(6)))
                continue

        if "SECTION" in parsedLine:
            if snippetMode:
                listErrors.append(
                    (
                        "codeerror",
                        i,
                        appState.getT(7),
                    )
                )
                continue
            lastLineType = "SECTION"
            if "SNIPPET_DUMMY_SECTION" in bytecode["__MEMINFOSTART"]:
                bytecode["__MEMINFOSTART"] = maxAddrBySection.copy()
                bytecode["__MEMINFOEND"] = maxAddrBySection.copy()

            if currentSection is not None:
                maxAddrBySection[currentSection] = currentAddr
                bytecode["__MEMINFOEND"][currentSection] = currentAddr

            if parsedLine["SECTION"] == "INTVEC":
                currentSection = "INTVEC"
                if viewedSections.intersection(("CODE", "DATA")):
                    listErrors.append(
                        (
                            "codeerror",
                            i,
                            appState.getT(8),
                        )
                    )
                    return None, None, None, None, None, listErrors
                currentAddr = max(memory_configs[memLayout]["INTVEC"], currentAddr)
            elif parsedLine["SECTION"] == "CODE":
                currentSection = "CODE"
                if "DATA" in viewedSections:
                    listErrors.append(
                        (
                            "codeerror",
                            i,
                            appState.getT(9),
                        )
                    )
                    return None, None, None, None, None, listErrors
                currentAddr = max(memory_configs[memLayout]["CODE"], currentAddr)
            elif parsedLine["SECTION"] == "DATA":
                currentSection = "DATA"
                currentAddr = max(memory_configs[memLayout]["DATA"], currentAddr)

            if currentSection in viewedSections:
                listErrors.append(
                    (
                        "codeerror",
                        i,
                        appState.getT(10).format(currentSection),
                    )
                )
                continue
            else:
                viewedSections.add(currentSection)

            # Ensure word alignement
            currentAddr += 4 - currentAddr % 4 if currentAddr % 4 != 0 else 0
            bytecode[currentSection] = bytearray()
        else:
            addrToLine[max(currentAddr, 0)].append(i)

        if "ASSERTION" in parsedLine:
            if lastLineType is None or lastLineType in ("LABEL", "SECTION"):
                assertions[currentAddr].append(("BEFORE", i, parsedLine["ASSERTION"]))
            elif lastLineType == "BYTECODE":
                assertions[currentAddr - 4].append(
                    ("AFTER", i, parsedLine["ASSERTION"])
                )

        if ("LABEL" in parsedLine or "BYTECODE" in parsedLine) and currentAddr == -1:
            # No section defined, but we have a label or an instruction; we switch to snippet mode
            snippetMode = True
            currentAddr = 0
            currentSection = "SNIPPET_DUMMY_SECTION"
            bytecode[currentSection] = bytearray()

        if "LABEL" in parsedLine:
            if parsedLine["LABEL"] in labelsAddr:
                # This label was already defined
                firstaddr = addrToLine[labelsAddr[parsedLine["LABEL"]]][0]
                listErrors.append(
                    (
                        "codeerror",
                        i,
                        appState.getT(11).format(
                            parsedLine["LABEL"], firstaddr + 1
                        ),
                    )
                )
            labelsAddr[parsedLine["LABEL"]] = currentAddr
            lastLineType = "LABEL"
            if "BYTECODE" not in parsedLine:
                lineToAddr[i] = [currentAddr]

        if "BYTECODE" in parsedLine:
            # The BYTECODE field contains a tuple
            # The first element is a bytes object containing the bytecode (so we just add it to the current one)
            # The second is the eventual missing dependencies (when using a label in a jump or mem operation)
            bytecode[currentSection].extend(parsedLine["BYTECODE"][0])
            # If there are some unresolved dependencies, we note it
            dep = parsedLine["BYTECODE"][1]
            if dep is not None:
                unresolvedDepencencies[(currentSection, currentAddr, i)] = dep
                if dep[0] in ("addrptr", "const"):
                    # We will need to add a constant with this label address
                    # or this constant at the end of the section
                    requiredLabelsPtr.append((dep[1], i))
            # We add the size of the object to the current address (so this always points to the address of the next element)
            tmpAddr = currentAddr
            for tmpAddr in range(
                max(currentAddr, 0),
                max(currentAddr, 0) + len(parsedLine["BYTECODE"][0]),
                4,
            ):
                addrToLine[tmpAddr].append(i)
            lineToAddr[i] = [
                currentAddr + li for li in range(len(parsedLine["BYTECODE"][0]))
            ]
            currentAddr += len(parsedLine["BYTECODE"][0])
            lastLineType = "BYTECODE"
            totalMemAllocated += len(parsedLine["BYTECODE"][0])
            if (
                currentSection == "INTVEC"
                and currentAddr > memory_configs[memLayout]["CODE"]
            ):
                listErrors.append(
                    (
                        "codeerror",
                        i,
                        appState.getT(12),
                    )
                )

        if totalMemAllocated > getSetting("maxtotalmem"):
            return (
                None,
                None,
                None,
                None,
                None,
                [
                    (
                        "error",
                        appState.getT(13).format(
                            getSetting("maxtotalmem")
                        ),
                    )
                ],
            )

    maxAddrBySection[currentSection] = currentAddr
    bytecode["__MEMINFOEND"][currentSection] = currentAddr

    if "SNIPPET_DUMMY_SECTION" not in bytecode:
        if "INTVEC" not in bytecode:
            listErrors.append(
                (
                    "codeerror",
                    0,
                    appState.getT(14),
                )
            )
            return None, None, None, None, None, listErrors
        if "CODE" not in bytecode:
            listErrors.append(
                (
                    "codeerror",
                    0,
                    appState.getT(15),
                )
            )
            return None, None, None, None, None, listErrors
        if "DATA" not in bytecode:
            listErrors.append(
                (
                    "codeerror",
                    0,
                    appState.getT(16),
                )
            )
            return None, None, None, None, None, listErrors

    # We resolve the pointer dependencies (that is, the instructions using =label)
    labelsPtrAddr = {}
    sectionToUse = (
        "CODE" if "CODE" in bytecode["__MEMINFOSTART"] else "SNIPPET_DUMMY_SECTION"
    )
    # At the end of the CODE section, we write all the label adresses referenced
    currentAddr = bytecode["__MEMINFOEND"][sectionToUse]
    for labelPtr, lineNo in requiredLabelsPtr:
        isConst = isinstance(labelPtr, int)
        if not isConst and labelPtr not in labelsAddr:
            listErrors.append(
                (
                    "codeerror",
                    lineNo,
                    appState.getT(17).format(
                        labelPtr
                    ),
                )
            )
            continue

        if labelPtr in labelsPtrAddr:
            # Already added (it's just referenced at two different places)
            continue

        if isConst:
            bytecode[sectionToUse].extend(struct.pack("<I", labelPtr & 0xFFFFFFFF))
        else:
            bytecode[sectionToUse].extend(
                struct.pack("<I", labelsAddr[labelPtr] & 0xFFFFFFFF)
            )
        labelsPtrAddr[labelPtr] = currentAddr
        currentAddr += 4
    bytecode["__MEMINFOEND"][sectionToUse] = currentAddr

    if len(listErrors) > 0:
        # At least one line did not assemble, we cannot continue
        return None, None, None, None, None, listErrors

    # At this point, all dependencies should have been resolved (e.g. all the labels should have been seen)
    # We fix the bytecode of the affected instructions
    for (sec, addr, line), depInfo in unresolvedDepencencies.items():
        # We retrieve the instruction and fit it into a 32 bit integer
        reladdr = addr - bytecode["__MEMINFOSTART"][sec]
        instrInt = struct.unpack("<I", bytecode[sec][reladdr : reladdr + 4])[0]
        if depInfo[0] in ("addr", "addrptr", "const"):
            # A LDR/STR on a label or a label's address
            dictToLookIn = labelsAddr if depInfo[0] == "addr" else labelsPtrAddr
            try:
                addrToReach = dictToLookIn[depInfo[1]]
            except KeyError:  # The label was never defined
                listErrors.append(
                    (
                        "codeerror",
                        line,
                        appState.getT(18).format(depInfo[1]),
                    )
                )
                continue

            diff = addrToReach - (addr + pcoffset)
            maxoffset = depInfo[2]
            if abs(diff) > maxoffset - 1:
                # Offset too big to be encoded as immediate
                listErrors.append(
                    (
                        "codeerror",
                        line,
                        appState.getT(19).format(
                            depInfo[1], diff
                        ),
                    )
                )
                continue
            if diff >= 0:
                instrInt |= 1 << 23
            if maxoffset == 4096:
                # LDR/STR case
                instrInt |= abs(diff)
            else:
                # LDRH/SB/SH case
                diff = abs(diff)
                instrInt |= diff & 0xF
                instrInt |= ((diff >> 4) & 0xF) << 8

        elif depInfo[0] == "addrbranch":
            # A branch on a given label
            # This is different than the previous case, since the offset is divided by 4
            # (when taking the branch, the offset is "shifted left two bits, sign extended to 32 bits"
            try:
                addrToReach = labelsAddr[depInfo[1]]
            except KeyError:  # The label was never defined
                listErrors.append(
                    (
                        "codeerror",
                        line,
                        appState.getT(20).format(depInfo[1]),
                    )
                )
                continue
            diff = addrToReach - (addr + pcoffset)
            if diff % 4 != 0:
                listErrors.append(
                    (
                        "codeerror",
                        line,
                        appState.getT(21).format(
                            depInfo[1], diff
                        ),
                    )
                )

            instrInt |= (diff // 4) & 0xFFFFFF
        else:
            assert False

        # We put back the modified instruction in the bytecode
        b = struct.pack("<I", instrInt)
        bytecode[sec][reladdr : reladdr + 4] = b

    if len(listErrors) > 0:
        # At least one line did not assemble, we cannot continue
        return None, None, None, None, None, listErrors

    # No errors
    return bytecode, addrToLine, lineToAddr, assertions, snippetMode, []
