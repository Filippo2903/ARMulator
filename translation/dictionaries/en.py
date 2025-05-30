# Dictionary in English
"""
The English dictionary for translation
"""

dict = {
    "abstractOp": [
        "Internal error: ",
        "<li>Checks if the condition {} is met</li>\n",
        "The instruction is invalid (the requested condition does not exist)"
    ],

    "branchOp": [
        "The bytecode at this address does not correspond to any valid instruction (1)",
        "<li>Copies the value of {}-4 (the address of the next instruction) into {}</li>\n",
        "<li>Subtracts the value {} from {}</li>\n",
        "<li>Adds the value {} to {}</li>\n",
        "<li>Copies the value from {} into {}</li>\n"
    ],

    "dataOp": [
        "The bytecode at this address does not correspond to any valid instruction (2)",
        "The constant {}",
        "Register {} {}",
        "<li>Performs a bitwise AND operation between:</li>\n",
        "<li>Performs an exclusive OR (XOR) operation between:</li>\n",
        "<li>Performs a subtraction (A-B) between:</li>\n",
        "<li>Performs a reverse subtraction (B-A) between:</li>\n",
        "<li>Performs an addition (A+B) between:</li>\n",
        "<li>Performs an addition with carry (A+B+carry) between:</li>\n",
        "<li>Performs a subtraction with borrow (A-B+carry) between:</li>\n",
        "<li>Performs a reverse subtraction with borrow (B-A+carry) between:</li>\n",
        "<li>Performs a bitwise OR operation between:</li>\n",
        "<li>Reads the value of:</li>\n",
        "<li>Performs a bitwise AND NOT operation between:</li>\n",
        "<li>Performs a bitwise NOT operation on:</li>\n",
        "Invalid mnemonic: {}",
        "<ol type=\"A\"><li>Register {}</li><li>{}</li></ol>\n",
        "<ol type=\"A\"><li>Register {}</li>\n",
        "<li>Copies the current SPSR into CPSR</li>\n",
        "<li>Updates the ALU flags based on the result of the operation</li>\n",
        "<li>Writes the result into {}</li>",
        "Invalid mnemonic: {}",
        "Using PC as destination register with flag update is forbidden in User mode!",
        "SPSR should be copied into CPSR here, but the mode contained in SPSR is invalid!"
    ],

    "halfSignedMemOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Uses the value of register {} as the base address</li>\n",
        "<li>Adds constant {} to the base address</li>\n",
        "<li>Subtracts constant {} from the base address</li>\n",
        "<li>Adds register {} to the base address</li>\n",
        "<li>Subtracts register {} from the base address</li>\n",
        "<li>Reads {} from the obtained address (pre-increment) and stores the result in {} (LDR)</li>\n",
        "<li>Reads {} from the base address and stores the result in {} (LDR)</li>\n",
        "<li>Copies the value of bit {} into bits {} to 31 of the destination register</li>\n",
        " of the least significant byte",
        " of the two least significant bytes",
        "<li>Copies the value",
        " of register {} into memory at the address obtained in the previous step (pre-increment), over {} (STR)</li>\n",
        "<li>Copies the value",
        " of register {} into memory at the base address, over {} (STR)</li>\n",
        "<li>Writes the effective address into the base register {} (writeback mode)</li>\n",
        "Attempted read of {} bytes from invalid address {}: memory not initialized"
    ],

    "memOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Uses the value of register {} as the base address</li>\n",
        "<li>Adds constant {} to the base address</li>\n",
        "<li>Subtracts constant {} from the base address</li>\n",
        "<li>Adds register {} {} to the base address</li>\n",
        "<li>Subtracts register {} {} from the base address</li>\n",
        "1 byte",
        "{} bytes",
        "<li>Reads {} from the obtained address (pre-increment) and stores the result in {} (LDR)</li>\n",
        "<li>Reads {} from the base address and stores the result in {} (LDR)</li>\n",
        "<li>Copies the value of register {} into memory at the address obtained in the previous step (pre-increment), over {} (STR)</li>\n",
        "<li>Copies the value of register {} into memory at the base address, over {} (STR)</li>\n",
        "<li>Writes the effective address into the base register {} (writeback mode)</li>\n",
        "Attempted read of {} bytes from invalid address {}: memory not initialized"
    ],

    "mulLongOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Performs a {} multiplication and addition on 64 bits (A*B+[C,D]) between:</li>\n",
        "<ol type=\"A\"><li>Register {}</li>\n",
        "<li>Register {}</li>\n",
        "<li>Register {}</li>\n",
        "<li>Register {}</li></ol>\n",
        "<li>Performs a {} multiplication (A*B) between:</li>\n",
        "<ol type=\"A\"><li>Register {}</li>\n",
        "<li>Register {}</li></ol>\n",
        "<li>Updates the ALU flags based on the result of the operation</li>\n",
        "<li>Writes the 32 MSB of the result to R{} and the 32 LSB to R{}</li>"
    ],

    "mulOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Performs a multiplication followed by an addition (A*B+C) between:</li>\n",
        "<ol type=\"A\"><li>Register {}</li>\n",
        "<li>Register {}</li>\n",
        "<li>Register {}</li></ol>\n",
        "<li>Updates the ALU flags based on the result of the operation</li>\n",
        "<li>Performs a multiplication (A*B) between:</li>\n",
        "<ol type=\"A\"><li>Register {}</li>\n",
        "<li>Register {}</li></ol>\n",
        "<li>Updates the ALU flags based on the result of the operation</li>\n",
        "<li>Writes the result into R{}</li>"
    ],

    "multipleMemOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Reads the value of SP</li>\n",
        "<li>For each register in the following list, stores the value from the address pointed to by SP into the register, then increments SP by 4.</li>\n",
        "<li>Reads the value of SP</li>\n",
        "<li>For each register in the following list, decrements SP by 4, then stores the value of the register at the address pointed to by SP.</li>\n",
        "<li>Reads the value of {}</li>\n",
        "<li>For each register in the following list, stores the value from the address pointed to by {reg} into the register, then {incmode} {reg} by 4.</li>\n",
        "<li>Reads the value of {}</li>\n",
        "<li>For each register in the following list, {incmode} {reg} by 4, then stores the value of the register at the address pointed to by {reg}.</li>\n",
        "<li>Copies the current SPSR into CPSR</li>\n"
    ],

    "nopOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Does nothing</li><li>Seriously, nothing at all</li>"
    ],

    "psrOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Writes constant {} into {}</li>\n",
        "<li>Reads the value of {}</li>\n",
        "<li>Writes the 4 most significant bits of this value (which correspond to flags) into {}</li>\n",
        "<li>Reads the value of {}</li>\n",
        "<li>Writes this value into {}</li>\n",
        "<li>Reads the value of {}</li>\n",
        "<li>Writes the result into {}</li>\n",
        "Error: writing to SPSR in 'User' mode (this mode has no SPSR register)",
        "Error: bits ({:05b}) of the {} mode do not correspond to any valid mode!",
        "Error: attempting to change processor mode from a non-privileged mode!",
        "Error: reading SPSR in 'User' mode (this mode has no SPSR register)"
    ],

    "softInterruptOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Switches register bank to SVC</li>\n",
        "<li>Copies CPSR into SPSR_svc</li>\n",
        "<li>Copies PC into LR_svc</li>\n",
        "<li>Assigns 0x08 to PC</li>\n"
    ],

    "swapOp": [
        "The bytecode at this address does not correspond to any valid instruction",
        "<li>Reads {} from the address contained in {}</li>\n",
        "<li>Writes the least significant byte of register {} to the address contained in {}</li>\n",
        "<li>Writes the least significant byte of the original memory value into {}</li>\n",
        "<li>Writes the value of register {} to the address contained in {}</li>\n",
        "<li>Writes into {} the original value from the address contained in {}</li>\n",
        "Attempted read of {} bytes from invalid address {}: memory not initialized"
    ],

    "utils": [
        "shifted left (LSL mode)",
        "shifted right (LSR mode)",
        "shifted right (ASR mode)",
        "rotated right with carry (RRX mode)",
        "rotated right (ROR mode)",
        " by {} {}",
        " by the number of positions contained in {}"
    ],

    "assembler": [
        "Syntax error",
        "Range error",
        "Invalid instruction",
        "Actual PC behavior not implemented yet",
        "Invalid instruction format",
        "Unable to interpret the instruction",
        "Invalid instruction",
        "You cannot write an instruction before the first SECTION keyword; if you want to test a code snippet, do not declare any section.",
        "The INTVEC section must be defined before the CODE and DATA sections!",
        "The CODE section must be defined before the DATA section!",
        "The section '{}' is defined twice!",
        "The label '{}' is defined twice (first definition at line {})",
        "The declaration on this line causes the INTVEC section to overflow into the CODE section. Make sure you allocate the correct number of bytes (128 bytes maximum for the whole INTVEC section).",
        "The code requests a total allocation of more than {} bytes of memory, which is invalid.",
        "The INTVEC section is not declared anywhere (use 'SECTION INTVEC' at the beginning of the code)!",
        "The CODE section is not declared anywhere (use 'SECTION CODE')!",
        "The DATA section is not declared anywhere (use 'SECTION DATA' at the end of your code)!",
        "This line requests the address of the label {}, but it is not declared anywhere",
        "The label {} is not declared anywhere",
        "Access to the address identified by label {} is too far ({} bytes offset) to be encoded",
        "The label {} is not declared anywhere",
        "The label {} corresponds to an offset of {} bytes, which is not a multiple of 4, as required by ARM"
    ],

    "components": [
        "Invalid mode '{}'",
        "Register SPSR does not exist in 'User' mode!",
        "Register SPSR does not exist in 'User' mode!",
        "Attempt to read an instruction at an uninitialized address: {}",
        "Faulty memory read access at address {}",
        "Invalid access for a write of size {} at address {}"
    ],

    "history": [
        "End of history reached, unable to go higher!"
    ],

    "mainweb": [
        "Information unavailable",
        "Please assemble the code before performing this operation.",
        "Invalid memory address",
        "Invalid value: {}",
        "Invalid register: {}",
        "Invalid value: {}"
    ],

    "simulator": [
        "Error: the value of PC ({}) is invalid (it must be a multiple of 4)!",
        "Information unavailable",
        "Instruction",
        "Error: {} should be {} (the value of register R{}), but it is {}\n",
        "Error: {} should be {}, but it is {}\n",
        "Error: the memory address {} should contain {} (the value of register R{}), but it contains {}\n",
        "Error: the memory address {} should contain {}, but it contains {}\n",
        "Error: the flag {} should indicate {}, but it indicates {}\n",
        "Unknown or impossible to interpret assertion: ({}, {})!"
    ],

    "tokenizer": [
        "(01) Invalid character (line {}, column {}) : {}",
        "(02) Invalid character (line {}, column {}) : {}",
        "(03) Invalid character (line {}, column {}) : {}",
        "(04) Invalid character (line {}, column {}) : {}",
        "(05) Invalid character (line {}, column {}) : {}",
        "(06) Invalid character (line {}, column {}) : {}",
        "(07) Invalid character (line {}, column {}) : {}",
        "(08) Invalid character (line {}, column {}) : {}",
        "(09) Invalid character (line {}, column {}) : {}",
        "(10) Invalid character (line {}, column {}) : {}",
        "(11) Invalid character (line {}, column {}) : {}",
        "(12) Invalid character (line {}, column {}) : {}",
        "(12b) Invalid character (line {}, column {}) : {}",
        "(13) Invalid character (line {}, column {}) : {}",
        "(07b) Invalid character (line {}, column {}) : {}",
        "(14) Invalid character (line {}, column {}) : {}",
        "(15) Invalid character (line {}, column {}) : {}",
        "(16) Invalid character (line {}, column {}) : {}",
        "(17) Invalid character (line {}, column {}) : {}",
        "(18) Invalid character (line {}, column {}) : {}",
        "(19) Invalid character (line {}, column {}) : {}",
        "(20) Invalid character (line {}, column {}) : {}",
        "(21) Invalid character (line {}, column {}) : {}",
        "(22) Invalid character (line {}, column {}) : {}",
        "(23) Invalid character (line {}, column {}) : {}",
        "(24) Invalid character (line {}, column {}) : {}",
        "(25) Invalid character (line {}, column {}) : {}",
        "(26) Invalid character (line {}, column {}) : {}",
        "(G) Invalid character (line {}, column {}) : {}"
    ],

    "yaccparser": [
        "A label must start with a lowercase or uppercase letter (not with a number)",
        "Invalid instruction: \"{}\". Please refer to the simulator manual for the list of accepted instructions.",
        "Register R{}{} does not exist",
        "The instruction {} requires a register as the first argument",
        "Registers and/or constants used in an operation must be separated by a comma",
        "Registers and/or constants used in an operation must be separated by a comma",
        "The instruction {} requires 3 arguments",
        "Register R{}{} does not exist",
        "Register R{}{} does not exist",
        "TEST",
        "Cannot encode the following constant or its inverse in an instruction {}: {}",
        "Cannot encode the following constant in an instruction {}: {}",
        "Register R{}{} does not exist",
        "A comma is required before the shift operation",
        "Invalid shift {} without a parameter (register or constant) specifying the shift",
        "Cannot encode a negative shift ({}) in an instruction (use another shift operator to achieve the same effect)",
        "Cannot encode the shift {} in an instruction (it must be less than 32)",
        "An instruction {} does not accept a shift on its offset register",
        "The requested shift of {} in the instruction is too large to be encoded (it must be less than 256)",
        "It is forbidden to use STR with a label address as the target. For example, 'STR R0, a' is valid, but not 'STR R0, =a'.",
        "It is forbidden to use PC as the base register when writeback is enabled.",
        "In writeback mode, it is forbidden to use the same register as both the destination and the base address.",
        "The requested shift of {} in the instruction is too large to be encoded (it must be less than 4096)",
        "A shift operation must be preceded by a comma.",
        "PC cannot be used as a shift register!",
        "It is forbidden to use PC as the base register in post-increment mode!",
        "The requested shift of {} in the instruction is too large to be encoded (it must be less than 4096)",
        "The target of a branch must be a label (or, for BX, a register). A label cannot start with a number.",
        "An instruction {} must specify at least one register in its list.",
        "It is forbidden to use PC as the base register in a multiple memory operation!",
        "Cannot directly assign a constant to a status register. Only flags can be directly modified by adding the _flg suffix to the status register.",
        "Cannot encode the following constant in an instruction {}: {}",
        "An instruction {} cannot receive a constant as the last argument, only a register.",
        "An instruction {} cannot receive more than 3 registers as arguments.",
        "An instruction {} cannot receive a constant as the last argument, only a register.",
        "The PC register cannot be used.",
        "Register R{} cannot be used more than once.",
        "A variable can have the following sizes (in bits): 8, 16, or 32. {} is not a valid size",
        "A variable assignment must be followed by a size in bits (for example ASSIGN32 or ASSIGN8)",
        "A variable can have the following sizes (in bits): 8, 16, or 32. {} is not a valid size",
        "A variable allocation can only be followed by the number of elements. Use ASSIGN if you want to assign specific values.",
        "Memory allocation request is too large. The maximum allowed is 8 KB (8192 bytes), but the declaration requests {} bytes.",
        "A variable allocation must be followed by a size in bits (for example ALLOC32 or ALLOC8)"
    ]
}
