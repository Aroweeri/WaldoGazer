from enum import Enum

class CycleMode(Enum):
	sequential = 1   #get next from list, loop to beginning
	random = 3       #creates a random list of tiles without repeating
