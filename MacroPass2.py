class MacroPass2:
    def __init__(self, program, mnt, mdt, ala):
        self.program = program
        self.mnt = mnt      # Macro Name Table from Pass 1
        self.mdt = mdt      # Macro Definition Table from Pass 1
        self.ala = ala      # Argument List Array from Pass 1
        self.expanded_code = []  # Stores the expanded code after macro expansion

    def pass_two(self):
        for line in self.program:
            tokens = line.strip().split()

            # Check if line is a macro invocation
            if tokens[0] in self.mnt:
                macro_name = tokens[0]
                self.expand_macro(macro_name, tokens[1:])
            else:
                # Add regular assembly instructions directly to the expanded code
                self.expanded_code.append(line)

    def expand_macro(self, macro_name, arguments):
        """Expands a macro by substituting arguments and adding it to the expanded code."""
        mdt_index = self.mnt[macro_name]
        ala_index = list(self.mnt.keys()).index(macro_name)  # Find the ALA entry for this macro
        current_ala = self.ala[ala_index]

        # Map provided arguments to the ALA
        arg_map = {}
        for i, arg in enumerate(arguments):
            # Substitute arguments based on the ALA position
            ala_key = list(current_ala.keys())[i]
            arg_map[current_ala[ala_key]] = arg

        # Iterate through the MDT, starting from the macro's entry point
        i = mdt_index
        while self.mdt[i] != "MEND":
            line = self.mdt[i]
            tokens = line.split()

            # Substitute any ALA indices in the line with actual arguments
            expanded_line = []
            for token in tokens:
                if token in arg_map:
                    expanded_line.append(arg_map[token])
                else:
                    expanded_line.append(token)

            self.expanded_code.append(" ".join(expanded_line))
            i += 1

    def display_expanded_code(self):
        print("Expanded Assembly Code:")
        for line in self.expanded_code:
            print(line)


# Sample macro data and program (normally these would be obtained from Pass 1)
program = [
    "START 100",
    "M1 10, 20, &B=CREG",
    "M2 100, 200, &V=AREG, &U=BREG",
    "END"
]

# Assuming the following tables from Pass 1
mnt = {'M1': 0, 'M2': 4}
mdt = [
    "MOVER &A, &X",
    "ADD &A, ='1'",
    "MOVER &B, &Y",
    "ADD &B, ='5'",
    "MOVER &U, &P",
    "MOVER &V, &Q",
    "ADD &U, ='15'",
    "ADD &V, ='10'",
    "MEND"
]
ala = [
    {'&X': '#0', '&Y': '#1', '&A': '#2', '&B': '#3'},
    {'&P': '#0', '&Q': '#1', '&U': '#2', '&V': '#3'}
]

# Run Pass 2 and display the expanded assembly code
macro_expander = MacroPass2(program, mnt, mdt, ala)
macro_expander.pass_two()
macro_expander.display_expanded_code()
