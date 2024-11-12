# Simulated output from Pass 1
symbol_table = {
    'START': 100,
    'A': 100,
    'L2': 108,
    'L': 110,
    'B': 120,
    'L1': 128,
    'C': 133
}
literal_table = {
    "='5'": 105,
    "='10'": 106,
    "='15'": 111
}
pool_table = [0, 2]  # Indicates the starting index of each literal pool
intermediate_code = [
    (100, 'START', ['100']),
    (100, 'DS', ['5']),
    (105, 'LOAD', ['A']),
    (106, 'ADD', ['AREG', "='5'"]),
    (107, 'MULT', ['BREG', "='10'"]),
    (108, 'TRANS', ['L']),
    (109, 'PRINT', ['L1']),
    (110, 'LTORG', []),
    (111, 'ADD', ['AREG', "='5'"]),
    (112, 'SUB', ['BREG', "='15'"]),
    (113, 'ADD', ['B']),
    (120, 'EQU', ['L+10']),
    (128, 'DS', ['5']),
    (133, 'DC', ['10']),
    (134, 'STOP', []),
    (135, 'END', [])
]

# Opcode Table (hypothetical example)
opcode_table = {
    'START': '00',
    'DS': '01',
    'LOAD': '02',
    'ADD': '03',
    'MULT': '04',
    'TRANS': '05',
    'PRINT': '06',
    'LTORG': '07',
    'SUB': '08',
    'EQU': '09',
    'ORIGIN': '10',
    'DC': '11',
    'STOP': '12',
    'END': '13'
}

# Pass 2 processing
final_machine_code = []

for address, opcode, operands in intermediate_code:
    if opcode == 'START':
        # Handle START: set location counter, no machine code needed
        final_machine_code.append(f"{address} {opcode_table[opcode]} {operands[0]}")
        
    elif opcode == 'DS':
        # DS reserves space; typically no machine code output
        size = int(operands[0])
        final_machine_code.append(f"{address} {opcode_table[opcode]} {size}")

    elif opcode == 'DC':
        # DC defines constant value at a given address
        constant = operands[0]
        final_machine_code.append(f"{address} {opcode_table[opcode]} {constant}")

    elif opcode in opcode_table:
        # General case for opcodes with registers and memory addresses
        operand_str = ""
        for operand in operands:
            if operand in symbol_table:
                operand_str += f"{symbol_table[operand]} "
            elif operand in literal_table:
                operand_str += f"{literal_table[operand]} "
            else:
                operand_str += f"{operand} "  # Register or immediate value

        final_machine_code.append(f"{address} {opcode_table[opcode]} {operand_str.strip()}")

    elif opcode == 'LTORG':
        # LTORG handles literals
        for literal, lit_address in literal_table.items():
            if lit_address >= address:
                final_machine_code.append(f"{lit_address} {opcode_table['DC']} {literal}")

    elif opcode == 'EQU':
        # EQU defines the address of a symbol based on an expression
        expression = operands[0]
        for symbol, addr in symbol_table.items():
            expression = expression.replace(symbol, str(addr))
        resolved_address = eval(expression)
        symbol_table[operands[0]] = resolved_address
        final_machine_code.append(f"{address} {opcode_table[opcode]} {resolved_address}")

    elif opcode == 'ORIGIN':
        # ORIGIN sets the location counter to a specific address
        expression = operands[0]
        for symbol, addr in symbol_table.items():
            expression = expression.replace(symbol, str(addr))
        location_counter = eval(expression)
        final_machine_code.append(f"{address} {opcode_table[opcode]} {location_counter}")

    elif opcode == 'STOP':
        # STOP opcode, typically indicates end of processing
        final_machine_code.append(f"{address} {opcode_table[opcode]}")

    elif opcode == 'END':
        # END indicates the end of the program
        final_machine_code.append(f"{address} {opcode_table[opcode]}")

# Print final machine code in table format
print("Final Machine Code:")
print("| Address | Opcode | Operands      |")
print("|---------|--------|---------------|")
for line in final_machine_code:
    print(line)
