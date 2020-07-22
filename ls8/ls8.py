#!/usr/bin/env python3

"""Main."""

#  Running CPU in a seperate file. 
import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()