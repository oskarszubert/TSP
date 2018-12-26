"""
TSP by Oskar Szubert
"""
import sys
from UserInterface import *

if __name__ == '__main__':
    if len(sys.argv) == 1:
        ui = UserInterface(1)
    else:
        ui = UserInterface( int(sys.argv[1]) )
