'''Maze tests'''

import unittest
from maze_master.maze import Direction

class DirectionTest(unittest.TestCase):
  ''' Test Direction class features'''
  def test_invert(self):
    '''Test the inversion of the direction'''
    self.assertEqual(Direction.South, Direction.North.invert())
    self.assertEqual(Direction.West, Direction.East.invert())
    self.assertEqual(Direction.North, Direction.South.invert())
    self.assertEqual(Direction.East, Direction.West.invert())
