"""CPU functionality."""

import sys

LDI = 0b10000010 # LDI R0,8
PRN = 0b01000111 # PRN R0
HLT = 0b00000001 # HLT
MUL = 0b10100010 # MUL R0,R1
POP = 0b01000110 
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01011010
JNE = 0b01010110

SP = 7

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

        self.halt = False

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            print(self.reg[reg_a])
        
        elif op == "DIV": 
            self.reg[reg_a] //= self.reg[reg_b]
        
        # alu part for the CMP(Computer Management Process) operation
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                # Set the Equal E flag to 1 
                pass
            elif self.reg[reg_a] < self.reg[reg_b]:
                # Set the less-than L flag to 1 
                pass
            elif self.reg[reg_a] > self.reg[reg_b]:
                # set the greater-than flag to 1
                pass
            else:
                # set the Equal E flag to 0
                pass

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):

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

            elif instructor_register == PUSH:
                index_of_the_register = self.ram_read(self.pc + 1)
                val = self.reg[index_of_the_register]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = val

            elif instructor_register == POP:
                index_of_the_register = self.ram_read(self.pc + 1)
                val = self.ram[self.reg[SP]]
                self.reg[index_of_the_register] = val
                self.reg[SP] += 1

            elif instructor_register == CALL:
                # Push the address of the instruction direction
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                # Set the PC to the address at the given register
                index_of_the_register = self.ram[self.pc + 1]
                self.pc = self.reg[index_of_the_register]

            elif instructor_register == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1
            
            # Add the CMP instructions and equal flag to your LS-8
            elif instructor_register == CMP:
                # How do I add anything to the LS-8
                #  How do I call the alu?
                self.alu("CMP", argumentOne, argumentTwo)
                


            # Add the JMP instruction
            elif instructor_register == JMP:
                # Go the register that is given
                # What is the register that is given?
                # Set the PC to the address stored in the given register
                pass

            # Add the JEQ instruction
            elif instructor_register == JEQ:
                # if the equal flag is set to true, jump to the address stored in the given register
                # What is the equal flag, how do I find it?
                # What does to jump to the register mean?
                # How do I store the address in the given register?
                # Set the PC
                pass

            # Add the JNE instructions
            elif instructor_register == JNE:
                # If E flag is clear(false, 0), jump to the address stored in the given register
                pass

            else:
                print(f"program failed to run", "{0:b".format(instructor_register))
                sys.exit(1)


            self.pc += instruction_length