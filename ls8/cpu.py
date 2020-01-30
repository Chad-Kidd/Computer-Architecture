"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU.
        Add list properties to the `CPU` class to hold 256 bytes of memory and 8
        general-purpose registers.
        add properties for any internal registers you need, e.g. `PC`.
        """
        self.reg = [0] * 8         #register
        self.ram = [0] * 256       # changed ram from 8 to 256 
        self.pc = 0                #Program Counter, address of the currently executing instruction
        self.ir = None             #Instruction Register, contains a copy of the currently executing instruction
        self.hlt = 0b00000001      #from load() previously
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.mul = 0b10100010

    def load(self, filename):
        """Load a program into memory."""

        address = 0 #DO NOT TRY 1 or 2 haha

        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                print("NUM", num) #some zeros and ones
                if num == "":
                    continue #continue even if blank
                value = int(num, 2)
                print("VAL!!", value) #pretty cool stuff
                self.ram[address] = value
                print("RAM ADDRESS", address)
                address += 1 #iterates

        # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000, #_operands_ represents R0
#             0b00001000, #_operands_ represents value
#             0b01000111, # PRN R0
#             0b00000000, #_operands_ represents R0
#             0b00000001, # HLT
#         ]

    def ram_read(self, address):
        """
        should accept the address to read and return the value stored there.
        """
        return self.ram[address]

    def ram_write(self, value, address):
        """should accept a value to write, and the address to write it to."""
        self.ram[address] = value

   
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

        # print()

    def run(self):
        """Run the CPU.
        """

        running = True
        while running:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            IR = self.ram[self.pc] 
            HLT = self.hlt
            LDI = self.ldi
            PRN = self.prn
            MUL = self.mul

            if IR == HLT: 
                running = False
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3 
            elif IR == PRN:
                index = self.ram_read(IR +1)
                
                print(self.reg[index])
                print(sys.argv[1])
                self.pc += 2
                #Multiply the values in two registers together and store the result in reg A
            elif IR == MUL:
                self.alu('MUL', (operand_a), (operand_b))
                self.pc += 3 #DO NOT TRY ONE unless you want chaos
            else:
                print(f'Error: Unknown command: {IR}')