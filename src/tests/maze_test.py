'''Maze tests'''

import unittest
from maze_master.maze import Direction, Limit, Tile, Maze

class DirectionTest(unittest.TestCase):
  ''' Test Direction class features'''
  def test_invert(self):
    '''Test the inversion of the direction'''
    self.assertEqual(Direction.South, Direction.North.invert())
    self.assertEqual(Direction.West, Direction.East.invert())
    self.assertEqual(Direction.North, Direction.South.invert())
    self.assertEqual(Direction.East, Direction.West.invert())

class LimitTest(unittest.TestCase):
  '''Test Limit class features'''
  def test_constructor(self):
    '''Test the limit constructor'''
    limit = Limit()
    self.assertTrue(limit.is_blocked)

class TileTest(unittest.TestCase):
  '''Test Tile class features'''
  def test_constructor(self):
    '''Test constructor'''
    nort_limit = Limit()
    east_limit = Limit()
    south_limit = Limit()
    west_limit = Limit()
    tile = Tile(8, 42, nort_limit, east_limit, south_limit, west_limit)
    self.assertEqual(8, tile.position_x)
    self.assertEqual(42, tile.position_y)
    self.assertEqual(tile.north_limit, nort_limit)
    self.assertEqual(tile.east_limit, east_limit)
    self.assertEqual(tile.south_limit, south_limit)
    self.assertEqual(tile.west_limit, west_limit)

  def test_is_all_blocked_true(self):
    '''Test when is_all_blocked is true'''
    tile = Tile(0, 0, Limit(), Limit(), Limit(), Limit())
    self.assertTrue(tile.is_all_blocked)

  def test_is_all_blocked_false(self):
    '''Test when is_all_blocked is false'''
    not_blocked_limit = Limit()
    not_blocked_limit.is_blocked = False
    tile = Tile(0, 0, not_blocked_limit, Limit(), Limit(), Limit())
    self.assertFalse(tile.is_all_blocked())

class MazeTest(unittest.TestCase):
  '''Test Maze class features'''
  def test_constructor(self):
    '''Test a simple random maze'''
    maze = Maze(2, 2)
    # validate that shared limits are the same
    self.assertEqual(maze.tiles[0][0].east_limit, maze.tiles[1][0].west_limit)
    self.assertEqual(maze.tiles[0][1].east_limit, maze.tiles[1][1].west_limit)
    self.assertEqual(maze.tiles[0][0].south_limit, maze.tiles[0][1].north_limit)
    self.assertEqual(maze.tiles[1][0].south_limit, maze.tiles[1][1].north_limit)
    
    # validate external walls.
    self.assertTrue(maze.tiles[0][0].west_limit.is_blocked)
    self.assertTrue(maze.tiles[0][0].north_limit.is_blocked)
    self.assertTrue(maze.tiles[1][0].east_limit.is_blocked)
    self.assertTrue(maze.tiles[1][0].north_limit.is_blocked)
    self.assertTrue(maze.tiles[0][1].west_limit.is_blocked)
    self.assertTrue(maze.tiles[0][1].south_limit.is_blocked)
    self.assertTrue(maze.tiles[1][1].east_limit.is_blocked)
    self.assertTrue(maze.tiles[1][1].south_limit.is_blocked)
    # validate one of the four possible labyrinths.
    if maze.tiles[1][1].west_limit.is_blocked:
      self.assertFalse(maze.tiles[0][0].east_limit.is_blocked)
      self.assertFalse(maze.tiles[0][0].south_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].north_limit.is_blocked)
    elif maze.tiles[0][0].south_limit.is_blocked:
      self.assertFalse(maze.tiles[0][0].east_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].west_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].north_limit.is_blocked)
    elif maze.tiles[0][0].east_limit.is_blocked:
      self.assertFalse(maze.tiles[0][0].south_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].west_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].north_limit.is_blocked)
    elif maze.tiles[1][1].north_limit.is_blocked:
      self.assertFalse(maze.tiles[0][0].east_limit.is_blocked)
      self.assertFalse(maze.tiles[0][0].south_limit.is_blocked)
      self.assertFalse(maze.tiles[1][1].west_limit.is_blocked)
