# Initialize tables and counters
symbol_table = {}
literal_table = []
pool_table = []
intermediate_code = []
location_counter = 100
literal_counter = 0

# Sample Assembly Code as list of instructions
assembly_code = [
    ("START", "100"),
    ("A", "DS", "3"),
    ("L1", "MOVEM", "AREG", "B"),
    ("", "ADD", "AREG", "C"),
    ("", "MOVER", "AREG", "='12'"),
    ("D", "EQU", "A+1"),
    ("", "LTORG"),
    ("L2", "PRINT", "D"),
    ("", "ORIGIN", "A-1"),
    ("", "MOVER", "AREG", "='5'"),
    ("C", "DC", "'5'"),
    ("", "ORIGIN", "L2+1"),
    ("", "STOP"),
    ("B", "DC", "'19'"),
    ("", "END")
]

# Pass 1: First scan to define all labels
for line in assembly_code:
    label, opcode, *operands = line

    # START Directive: Set the initial location counter
    if opcode == "START":
        location_counter = int(operands[0])
        intermediate_code.append((location_counter, opcode, operands))

    # Label Definitions (symbolic addresses)
    elif label:
        if opcode in ["DS", "DC"]:
            symbol_table[label] = location_counter
        else:
            symbol_table[label] = location_counter
            location_counter += 1

# Reset the location counter for the second pass
location_counter = 100

# Pass 1: Second scan for processing directives and instructions
for line in assembly_code:
    label, opcode, *operands = line

    # Process each line based on the opcode type
    if opcode == "START":
        location_counter = int(operands[0])
        intermediate_code.append((location_counter, opcode, operands))

    elif opcode == "DS":
        # Allocate space and add to symbol table
        symbol_table[label] = location_counter
        location_counter += int(operands[0])

    elif opcode == "DC":
        # Define constant and move location counter
        symbol_table[label] = location_counter
        intermediate_code.append((location_counter, opcode, operands))
        location_counter += 1

    elif opcode in ["MOVEM", "MOVER", "ADD", "PRINT", "STOP"]:
        if label and label not in symbol_table:
            symbol_table[label] = location_counter
        intermediate_code.append((location_counter, opcode, operands))
        location_counter += 1

    elif opcode == "EQU":
        # EQU directive processing with expression evaluation
        expression = operands[0]
        for symbol, addr in symbol_table.items():
            expression = expression.replace(symbol, str(addr))
        symbol_table[label] = eval(expression)

    elif opcode == "LTORG":
        # Process literals by adding them to symbol table and intermediate code
        for literal in literal_table:
            if literal not in symbol_table:
                symbol_table[literal] = location_counter
                intermediate_code.append((location_counter, "DC", literal))
                location_counter += 1
        pool_table.append(literal_counter)
        literal_table = []

    elif opcode == "ORIGIN":
        # Update location counter based on ORIGIN directive
        expression = operands[0]
        for symbol, addr in symbol_table.items():
            expression = expression.replace(symbol, str(addr))
        location_counter = eval(expression)

    elif opcode == "END":
        # Process remaining literals at END
        for literal in literal_table:
            if literal not in symbol_table:
                symbol_table[literal] = location_counter
                intermediate_code.append((location_counter, "DC", literal))
                location_counter += 1
        pool_table.append(literal_counter)
        break

    # Add literals to literal table for future processing
    for operand in operands:
        if operand.startswith("='"):
            if operand not in literal_table:
                literal_table.append(operand)
                literal_counter += 1

# Output tables in a readable format
# 1. Symbol Table
print("Symbol Table:")
print("| Symbol | Address |")
print("|--------|---------|")
for symbol, address in symbol_table.items():
    print(f"| {symbol:<6} | {address:<7} |")

# 2. Literal Table
print("\nLiteral Table:")
print("| Index | Literal | Address |")
print("|-------|---------|---------|")
for idx, literal in enumerate(literal_table):
    # Check if literal is defined in symbol_table to avoid KeyError
    address = symbol_table.get(literal, "Undefined")
    print(f"| L{idx:<5} | {literal:<7} | {address:<7} |")

# 3. Intermediate Code
print("\nIntermediate Code:")
print("| Address | Opcode | Operands      |")
print("|---------|--------|---------------|")
for line in intermediate_code:
    address, opcode, operands = line
    print(f"| {address:<8} | {opcode:<6} | {', '.join(operands):<13} |")

# 4. Pool Table
print("\nPool Table:")
print("| Pool Number | Start Index |")
print("|-------------|-------------|")
for idx, pool in enumerate(pool_table):
    print(f"| {idx+1:<11} | {pool:<11} |")
