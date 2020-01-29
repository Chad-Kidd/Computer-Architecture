"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256 
        # pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, #_operands_ represents R0
            0b00001000, #_operands_ represents value
            0b01000111, # PRN R0
            0b00000000, #_operands_ represents R0
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    #NOT SURE IF THESE GO THERE
   #`ram_read()` should accept the address to read and return the value stored there.

    def ram_read(self, address):
        return self.ram[address]

    #`ram_write()` should accept a value to write, and the address to write it to.

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        #check for halted
        halted = False
        # run while loop and conditionals
        while not halted:
            instruction = self.ram[self.pc]

            if instruction == 0b10000010: # LDI
                reg_number = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc +2)

                self.reg[reg_number] = value

                self.pc += 3 #should be 3

            elif instruction == 0b01000111: # PRN
                reg_number = self.ram_read(self.pc +1)
                print(self.reg[reg_number])
                self.pc += 2

            #condition for HALT
            elif instruction == 0b00000001: # HLT
                halted = True

                self.pc += 1

            else:
                print(f"Unknown instructions at index {self.pc}")
                sys.exit(1)

        ##syntax and indent block clean up. NOTE TO SELF be mindful
        # pass
        # pass
