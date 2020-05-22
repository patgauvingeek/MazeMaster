"""Tests for class Game"""

import os.path

import unittest
from maze_master.game import Game, Player, Position, RelativeDirection
from maze_master.maze import Direction, Limit, Maze, Tile

class RelativeDirectionTest(unittest.TestCase):
  def test_absolute(self):
    self.assertEqual(Direction.North, RelativeDirection.Forward.absolute(Direction.North)) 
    self.assertEqual(Direction.East, RelativeDirection.Forward.absolute(Direction.East))
    self.assertEqual(Direction.South, RelativeDirection.Forward.absolute(Direction.South))
    self.assertEqual(Direction.West, RelativeDirection.Forward.absolute(Direction.West))
    self.assertEqual(Direction.East, RelativeDirection.Right.absolute(Direction.North))
    self.assertEqual(Direction.South, RelativeDirection.Right.absolute(Direction.East))
    self.assertEqual(Direction.West, RelativeDirection.Right.absolute(Direction.South))
    self.assertEqual(Direction.North, RelativeDirection.Right.absolute(Direction.West))
    self.assertEqual(Direction.South, RelativeDirection.Back.absolute(Direction.North))
    self.assertEqual(Direction.West, RelativeDirection.Back.absolute(Direction.East)) 
    self.assertEqual(Direction.North, RelativeDirection.Back.absolute(Direction.South))
    self.assertEqual(Direction.East, RelativeDirection.Back.absolute(Direction.West))
    self.assertEqual(Direction.West, RelativeDirection.Left.absolute(Direction.North))
    self.assertEqual(Direction.North, RelativeDirection.Left.absolute(Direction.East))
    self.assertEqual(Direction.East, RelativeDirection.Left.absolute(Direction.South))
    self.assertEqual(Direction.South, RelativeDirection.Left.absolute(Direction.West))
    
  def test_relative(self):
    self.assertEqual(RelativeDirection.Forward, RelativeDirection.relative(Direction.North, Direction.North))
    self.assertEqual(RelativeDirection.Right, RelativeDirection.relative(Direction.North, Direction.East))
    self.assertEqual(RelativeDirection.Back, RelativeDirection.relative(Direction.North, Direction.South))
    self.assertEqual(RelativeDirection.Left, RelativeDirection.relative(Direction.North, Direction.West))
    self.assertEqual(RelativeDirection.Forward, RelativeDirection.relative(Direction.East, Direction.East))
    self.assertEqual(RelativeDirection.Right, RelativeDirection.relative(Direction.East, Direction.South))
    self.assertEqual(RelativeDirection.Back, RelativeDirection.relative(Direction.East, Direction.West))
    self.assertEqual(RelativeDirection.Left, RelativeDirection.relative(Direction.East, Direction.North))
    self.assertEqual(RelativeDirection.Forward, RelativeDirection.relative(Direction.South, Direction.South))
    self.assertEqual(RelativeDirection.Right, RelativeDirection.relative(Direction.South, Direction.West))
    self.assertEqual(RelativeDirection.Back, RelativeDirection.relative(Direction.South, Direction.North))
    self.assertEqual(RelativeDirection.Left, RelativeDirection.relative(Direction.South, Direction.East))
    self.assertEqual(RelativeDirection.Forward, RelativeDirection.relative(Direction.West, Direction.West))
    self.assertEqual(RelativeDirection.Right, RelativeDirection.relative(Direction.West, Direction.North))
    self.assertEqual(RelativeDirection.Back, RelativeDirection.relative(Direction.West, Direction.East))
    self.assertEqual(RelativeDirection.Left, RelativeDirection.relative(Direction.West, Direction.South))


class MazeMock:
  def __init__(self):
    self.width = 3
    self.depth = 3
    self.width_limits = [[Limit() for y in range(self.depth + 1)] for x in range(self.width + 1)]
    self.depth_limits = [[Limit() for y in range(self.depth + 1)] for x in range(self.width + 1)]
    self.tiles = [[Tile(x, y, self.depth_limits[x][y], self.width_limits[x+1][y], self.depth_limits[x][y+1], self.width_limits[x][y]) for y in range(self.depth)] for x in range(self.width)]

  def Unblock(self):
    for limits in self.width_limits:
      for widthLimit in limits:
        widthLimit.is_blocked = False
    for limits in self.depth_limits:
      for depthLimit in limits:
        depthLimit.is_blocked = False

class GameTest(unittest.TestCase):
  def test_add_remove_player(self):
    game = Game(3, 3)
    player = Player("Mike")
    game.add_player(player)
    self.assertEqual(player, game.players["Mike"])
    self.assertTrue(player in game.locations[game.start_position].Items)
    game.remove_player(player)
    self.assertFalse("Mike" in game.players)
    self.assertFalse(player in game.locations[game.start_position].Items)

  def test_player_cannot_move(self):
    game = Game(3, 3)
    game.maze = MazeMock()
    
    playerFoward = Player("TriedForward")
    game.add_player(playerFoward)
    game.move_player(playerFoward, RelativeDirection.Forward)
    self.assertEqual(Position(1, 1), playerFoward.position)
    self.assertEqual(Direction.North, playerFoward.Facing)

    playerRight = Player("TriedRight")
    game.add_player(playerRight)
    game.move_player(playerRight, RelativeDirection.Right)
    self.assertEqual(Position(1, 1), playerRight.position)
    self.assertEqual(Direction.North, playerRight.Facing)

    playerBack = Player("TriedBack")
    game.add_player(playerBack)
    game.move_player(playerBack, RelativeDirection.Back)
    self.assertEqual(Position(1, 1), playerBack.position)
    self.assertEqual(Direction.North, playerBack.Facing)

    playerLeft = Player("TriedLeft")
    game.add_player(playerLeft)
    game.move_player(playerLeft, RelativeDirection.Left)
    self.assertEqual(Position(1, 1), playerLeft.position)
    self.assertEqual(Direction.North, playerLeft.Facing)

  def test_player_can_move(self):
    game = Game(3, 3)
    game.maze = MazeMock()
    game.maze.Unblock()
    
    playerFoward = Player("TriedForward")
    game.add_player(playerFoward)
    game.move_player(playerFoward, RelativeDirection.Forward)
    self.assertEqual(Position(1, 0), playerFoward.position)
    self.assertEqual(Direction.North, playerFoward.Facing)

    playerRight = Player("TriedRight")
    game.add_player(playerRight)
    game.move_player(playerRight, RelativeDirection.Right)
    self.assertEqual(Position(2, 1), playerRight.position)
    self.assertEqual(Direction.East, playerRight.Facing)

    playerBack = Player("TriedBack")
    game.add_player(playerBack)
    game.move_player(playerBack, RelativeDirection.Back)
    self.assertEqual(Position(1, 2), playerBack.position)
    self.assertEqual(Direction.South, playerBack.Facing)

    playerLeft = Player("TriedLeft")
    game.add_player(playerLeft)
    game.move_player(playerLeft, RelativeDirection.Left)
    self.assertEqual(Position(0, 1), playerLeft.position)
    self.assertEqual(Direction.West, playerLeft.Facing)

  def test_render_picture(self):
    "Test render_picture(filename)"
    game = Game(3, 3)
    tile = game.maze.tiles[0][0]
    filename = "render_picture_test.png"
    game.render_picture(filename)
    try:
      self.assertTrue(os.path.isfile(filename))
    finally:
      os.remove(filename)

def JoinTest():
  if join([1], ", ", " or ") != "1":
    return Test.FAIL
  if join([1, 2, 3], ", ", " or ") != "1, 2 or 3":
    return Test.FAIL
  return Test.PASS
