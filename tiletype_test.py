import unittest
import tiletype

class TileTypeTest(unittest.TestCase):

	def test_tileType(self):
		self.assertEqual(tiletype.tileType(0, 3, 3), tiletype.TileType.CORNER, "Should be corner.")
		self.assertEqual(tiletype.tileType(1, 2, 2), tiletype.TileType.CORNER, "Should be corner.")
		self.assertEqual(tiletype.tileType(12, 4, 4), tiletype.TileType.CORNER, "Should be corner.")
		self.assertEqual(tiletype.tileType(15, 4, 4), tiletype.TileType.CORNER, "Should be corner.")
		self.assertEqual(tiletype.tileType(1, 3, 3), tiletype.TileType.EDGE, "Should be edge.")
		self.assertEqual(tiletype.tileType(3, 3, 3), tiletype.TileType.EDGE, "Should be edge.")
		self.assertEqual(tiletype.tileType(5, 3, 3), tiletype.TileType.EDGE, "Should be edge.")
		self.assertEqual(tiletype.tileType(7, 3, 3), tiletype.TileType.EDGE, "Should be edge.")
		self.assertEqual(tiletype.tileType(5, 4, 4), tiletype.TileType.CENTER, "Should be center.")
		self.assertEqual(tiletype.tileType(6, 4, 4), tiletype.TileType.CENTER, "Should be center.")
		self.assertEqual(tiletype.tileType(9, 4, 4), tiletype.TileType.CENTER, "Should be center.")
		self.assertEqual(tiletype.tileType(10, 4, 4), tiletype.TileType.CENTER, "Should be center.")

	def test_cornerType(self):
		self.assertEqual(tiletype.cornerType(0,3,3), tiletype.CornerType.TOPLEFT, "Should be top left corner.")
		self.assertEqual(tiletype.cornerType(2,3,3), tiletype.CornerType.TOPRIGHT, "Should be top right corner.")
		self.assertEqual(tiletype.cornerType(6,3,3), tiletype.CornerType.BOTTOMLEFT, "Should be bottom left corner.")
		self.assertEqual(tiletype.cornerType(8,3,3), tiletype.CornerType.BOTTOMRIGHT, "Should be bottom right corner.")
		self.assertEqual(tiletype.cornerType(0,100,100), tiletype.CornerType.TOPLEFT, "Should be top left corner.")
		self.assertEqual(tiletype.cornerType(99,100,100), tiletype.CornerType.TOPRIGHT, "Should be top right corner.")
		self.assertEqual(tiletype.cornerType(9900,100,100), tiletype.CornerType.BOTTOMLEFT, "Should be bottom left corner.")
		self.assertEqual(tiletype.cornerType(9999,100,100), tiletype.CornerType.BOTTOMRIGHT, "Should be bottom right corner.")
	
	def test_edgeType(self):
		self.assertEqual(tiletype.edgeType(1,3,3), tiletype.EdgeType.TOP, "Should be top edge.")
		self.assertEqual(tiletype.edgeType(3,3,3), tiletype.EdgeType.LEFT, "Should be left edge.")
		self.assertEqual(tiletype.edgeType(5,3,3), tiletype.EdgeType.RIGHT, "Should be right edge.")
		self.assertEqual(tiletype.edgeType(7,3,3), tiletype.EdgeType.BOTTOM, "Should be bottom edge.")
		self.assertEqual(tiletype.edgeType(2,3,4), tiletype.EdgeType.TOP, "Should be top edge.")
		self.assertEqual(tiletype.edgeType(4,3,4), tiletype.EdgeType.LEFT, "Should be left edge.")
		self.assertEqual(tiletype.edgeType(7,3,4), tiletype.EdgeType.RIGHT, "Should be right edge.")
		self.assertEqual(tiletype.edgeType(10,3,4), tiletype.EdgeType.BOTTOM, "Should be bottom edge.")

if __name__ == '__main__':
	unittest.main()
