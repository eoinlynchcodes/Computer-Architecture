"""CPU functionality."""

import sys

LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
HLT = 0b00000001 # HLT
MUL = 0b10100010 # MUL R0,R1


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        # pc (program counter) is current index for the ram
        # Of where we currently are on the ram
        self.pc = 0 
        self.halt = True 

    
    def ram_write(self, programIndex, value):
        self.ram[programIndex] = value 

    def ram_read(self, programIndex):
        return self.ram[programIndex]

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as theFile:
                for line in theFile:
                    comment_split = line.split('#')

                    num = comment_split[0].strip()

                    if num == '':
                        continue
                        
                    value = int(num, 2)

                    self.ram[address] = value

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
               
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        self.halt = False

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # Arithmetic Logic Unit: Definition, Design & Functions

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            print(self.reg[reg_a])
        
        elif op == "DIV": 
            self.reg[reg_a] //= self.reg[reg_b]

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
        # Read the memory address stores in register PC.
        # Store the result in IR / the Instructor Register.

        # exit an if else loop if a HLT instruction is encountered.

        # Add LDI instruction. Add a specified register to a specified value.

        # Add PRN instruction. See LS-8 spec. 

        while self.halt is False:
            instructor_register = self.ram[self.pc]
            instruction_length = ((instructor_register >> 6) & 0b11) + 1 # (bitshifted instruction)
            argumentOne = self.ram[self.pc + 1]
            argumentTwo = self.ram[self.pc + 2]
            
            # HLT
            if instructor_register == HLT:
                self.halt = True
            
            # LDI
            if instructor_register == LDI:
                self.reg[argumentOne] = argumentTwo
            
            # PRN
            elif instructor_register == PRN:
                print(self.reg[argumentOne])
            
            elif instructor_register == MUL:
                self.alu("MUL", argumentOne, argumentTwo)

            self.pc += instruction_length