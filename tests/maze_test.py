'''Maze tests'''

import Maze
import Test

def InvertTest():
  if Maze.Direction.North.invert() != Maze.Direction.South:
    return Test.FAIL
  if Maze.Direction.East.invert() != Maze.Direction.West:
    return Test.FAIL
  if Maze.Direction.South.invert() != Maze.Direction.North:
    return Test.FAIL
  if Maze.Direction.West.invert() != Maze.Direction.East:
    return Test.FAIL
  return Test.PASS

TESTS = [InvertTest]

Test.Execute(TESTS)
