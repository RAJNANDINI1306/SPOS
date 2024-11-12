class MacroPass1:
    def __init__(self, program):
        self.program = program
        self.mnt = {}  # Macro Name Table
        self.mdt = []  # Macro Definition Table
        self.ala = []  # Argument List Array
        self.is_macro = False
        self.current_macro = None

    def pass_one(self):
        for line in self.program:
            tokens = line.strip().split()

            # Start of a macro definition
            if tokens[0] == "MACRO":
                self.is_macro = True
                continue

            # End of a macro definition
            elif tokens[0] == "MEND":
                self.is_macro = False
                self.mdt.append("MEND")
                self.current_macro = None
                continue

            # Macro definition line
            elif self.is_macro:
                if self.current_macro is None:
                    # Start a new macro entry in MNT and initialize ALA
                    self.current_macro = tokens[0]
                    self.add_to_mnt(self.current_macro, len(self.mdt))
                    self.define_ala(tokens[1:])
                    self.mdt.append(f"{tokens[0]} {' '.join(self.replace_args(tokens[1:]))}")
                else:
                    # Process macro instructions and replace arguments with indices
                    self.mdt.append(f"{tokens[0]} {' '.join(self.replace_args(tokens[1:]))}")
            else:
                # Regular assembly instruction outside of macro definitions
                pass

    def add_to_mnt(self, macro_name, mdt_index):
        """Add the macro name and index to MNT."""
        self.mnt[macro_name] = mdt_index

    def define_ala(self, args):
        """Define argument list array (ALA) by extracting parameters."""
        ala_entry = {}
        for i, arg in enumerate(args):
            if '=' in arg:
                arg_name, default_value = arg.split('=')
                ala_entry[arg_name] = f"#{i}"
            else:
                ala_entry[arg] = f"#{i}"
        self.ala.append(ala_entry)

    def replace_args(self, args):
        """Replace arguments with their positions in the ALA."""
        if not self.ala:
            return args  # No ALA defined if outside a macro

        ala_entry = self.ala[-1]
        replaced_args = []
        for arg in args:
            if arg in ala_entry:
                replaced_args.append(ala_entry[arg])
            elif '=' in arg:
                # For default argument values
                arg_name, value = arg.split('=')
                if arg_name in ala_entry:
                    replaced_args.append(f"{ala_entry[arg_name]}={value}")
                else:
                    replaced_args.append(arg)
            else:
                replaced_args.append(arg)
        return replaced_args

    def display_tables(self):
        print("Macro Name Table (MNT):")
        for name, index in self.mnt.items():
            print(f"{name} -> MDT Index: {index}")

        print("\nMacro Definition Table (MDT):")
        for i, line in enumerate(self.mdt):
            print(f"{i}: {line}")

        print("\nArgument List Array (ALA):")
        for i, ala_entry in enumerate(self.ala):
            print(f"ALA for Macro #{i + 1}: {ala_entry}")


# Sample assembly code with macros
program = [
    "MACRO",
    "M1 &X, &Y, &A=AREG, &B=",
    "MOVER &A, &X",
    "ADD &A, ='1'",
    "MOVER &B, &Y",
    "ADD &B, ='5'",
    "MEND",
    "MACRO",
    "M2 &P, &Q, &U=CREG, &V=DREG",
    "MOVER &U, &P",
    "MOVER &V, &Q",
    "ADD &U, ='15'",
    "ADD &V, ='10'",
    "MEND",
    "START 100",
    "M1 10, 20, &B=CREG",
    "M2 100, 200, &V=AREG, &U=BREG",
    "END"
]

# Run Pass 1 and display the macro tables
macro_processor = MacroPass1(program)
macro_processor.pass_one()
macro_processor.display_tables()
