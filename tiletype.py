from enum import Enum

class TileType(Enum):
	CENTER = 1
	EDGE = 2
	CORNER = 3

class CornerType(Enum):
	TOPLEFT = 1
	TOPRIGHT = 2
	BOTTOMRIGHT = 3
	BOTTOMLEFT = 4

class EdgeType(Enum):
	TOP = 1
	RIGHT = 2
	BOTTOM = 3
	LEFT = 4

def tileType(i, numRows, numColumns):
	if(i == 0):
		return TileType.CORNER
	if(i == numRows*numColumns-1):
		return TileType.CORNER
	if(i == numColumns-1):
		return TileType.CORNER
	if(i == numRows*numColumns-numColumns):
		return TileType.CORNER

	if(i < numColumns):
		return TileType.EDGE
	if(i > (numRows*numColumns-numColumns) and i < (numRows*numColumns-1)):
		return TileType.EDGE
	if(i % numColumns == 0):
		return TileType.EDGE
	if(i % numColumns == numColumns-1):
		return TileType.EDGE

	return TileType.CENTER

def cornerType(i, numRows, numColumns):
	if(i == 0):
		return CornerType.TOPLEFT
	if(i == numRows*numColumns-1):
		return CornerType.BOTTOMRIGHT
	if(i == numColumns-1):
		return CornerType.TOPRIGHT
	if(i == numRows*numColumns-numColumns):
		return CornerType.BOTTOMLEFT

def edgeType(i, numRows, numColumns):
	if(i < numColumns):
		return EdgeType.TOP
	if(i > (numRows*numColumns-numColumns) and i < (numRows*numColumns-1)):
		return EdgeType.BOTTOM
	if(i % numColumns == 0):
		return EdgeType.LEFT
	if(i % numColumns == numColumns-1):
		return EdgeType.RIGHT
