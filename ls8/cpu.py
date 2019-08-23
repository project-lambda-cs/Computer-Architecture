"""CPU functionality."""

import sys


LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.register[7] = 255
        self.sp = self.register[7]

    def ram_read(self, address):
        return self.ram[address]

    def raw_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0

        if len(sys.argv) != 2:
            print("usage: file.py <filename>", file=sys.stderr)
            sys.exit(1)

        filename = sys.argv[1]

        try:

            with open(filename) as f:
                for line in f:
                    comment_line_split = line.split("#")
                    str_num = comment_line_split[0].strip()

                    if str_num == "":
                        continue

                    num = int(str_num, 2)
                    self.ram[address] = num
                    address += 1

                    # print(f'{num:08b}: {num}')

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found')
            sys.exit(2)

        # For now, we've just hardcoded a program:
        #[130, 0, 8, 71, 0, 1]
        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # check instruction / execute it, then
            # update PC
            if IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif IR == HLT:
                running = False
                self.pc += 1
            elif IR == PRN:
                print(f"PRN {self.register[operand_a]}")
                self.pc += 2
            elif IR == MUL:
                self.register[operand_a] *= self.register[operand_b]
                self.pc += 3
                # 8*9 72
            elif IR == PUSH:
                # decrement SP
                self.sp -= 1
                # get the register number operand
                regnum = operand_a
                # get the value from that register
                val = self.register[regnum]
                # store the val in memory at the SP
                self.ram[self.sp] = val
                # print(f"PUSH {self.register[operand_a]}")
                self.pc += 2

            elif IR == POP:
                # Copy the value out of memory where the sp is pointing
                val = self.ram[self.sp]
                # get the register number operand
                regnum = operand_a
                # store the value from the stack in the register number
                self.register[regnum] = val
                # print(f"POP {self.register[regnum]}")
                print(f"PRN {self.ram[self.sp:]}")
                # increment SP
                self.sp += 1
                self.pc += 2

            elif IR == CALL:
                self.sp -= 1
                self.ram[self.sp] = self.pc + 2  # <<
                regnum = operand_a
                self.pc = self.register[regnum]

            elif IR == RET:
                self.pc = self.ram[self.sp]
                self.sp += 1

            elif IR == ADD:
                self.register[operand_a] += self.register[operand_b]
                self.pc += 3

                # PC: Program Counter, address of the currently executing instruction special pursouse register
                # IR: Instruction Register, contains a copy of the currently executing instruction
                # LDI Set the value of a register to an integer.
                # SP Stack Pointer , general purpouse register


cpu = CPU()
cpu.load()
print(cpu.run())
# python3 cpu.py examples/print8.ls8 or nay other file form that dir
