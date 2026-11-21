
import os

SYMBOLS = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
    "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
    "R10": 10, "R11": 11, "R12": 12, "R13": 13,
    "R14": 14, "R15": 15,
    "SCREEN": 16384, "KBD": 24576
}

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111"
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


def clean_lines(source):
    cleaned = []

    for line_number, line in enumerate(source, 1):
        line = line.split("//")[0].strip()
        line = line.replace(" ", "").replace("\t", "")

        if line:
            cleaned.append((line_number, line))

    return cleaned


def first_pass(lines):
    symbols = SYMBOLS.copy()
    instructions = []
    rom_address = 0

    for line_number, line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]

            if not label or label in symbols:
                raise ValueError(
                    f"Line {line_number}: Invalid or duplicate label '{label}'"
                )

            symbols[label] = rom_address

        else:
            instructions.append((line_number, line))
            rom_address += 1

    return symbols, instructions


def assemble_instruction(line, line_number, symbols, next_variable):
    if line.startswith("@"):
        symbol = line[1:]

        if not symbol:
            raise ValueError(f"Line {line_number}: Empty A-instruction")

        if symbol.isdigit():
            address = int(symbol)
        else:
            if symbol not in symbols:
                symbols[symbol] = next_variable
                next_variable += 1

            address = symbols[symbol]

        if address < 0 or address > 32767:
            raise ValueError(
                f"Line {line_number}: A-instruction address out of range"
            )

        return format(address, "016b"), next_variable

    if line.count("=") > 1 or line.count(";") > 1:
        raise ValueError(f"Line {line_number}: Invalid C-instruction")

    if "=" in line:
        dest, rest = line.split("=")
    else:
        dest, rest = "", line

    if ";" in rest:
        comp, jump = rest.split(";")
    else:
        comp, jump = rest, ""

    if dest not in DEST:
        raise ValueError(f"Line {line_number}: Invalid destination '{dest}'")

    if comp not in COMP:
        raise ValueError(f"Line {line_number}: Invalid computation '{comp}'")

    if jump not in JUMP:
        raise ValueError(f"Line {line_number}: Invalid jump '{jump}'")

    binary = "111" + COMP[comp] + DEST[dest] + JUMP[jump]
    return binary, next_variable


def assemble_file(filename):
    with open(filename, "r") as file:
        source = file.readlines()

    lines = clean_lines(source)
    symbols, instructions = first_pass(lines)

    machine_code = []
    next_variable = 16

    for line_number, line in instructions:
        binary, next_variable = assemble_instruction(
            line, line_number, symbols, next_variable
        )
        machine_code.append(binary)

    output_file = os.path.splitext(filename)[0] + ".hack"

    with open(output_file, "w") as file:
        for code in machine_code:
            file.write(code + "\n")

    print("Successfully assembled:", filename)
    print("Output:", output_file)


def main():
    filename = input("Enter the ASM file path: ").strip().strip('"')

    try:
        assemble_file(filename)

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError as error:
        print("Assembler Error:", error)


if __name__ == "__main__":
    main()
