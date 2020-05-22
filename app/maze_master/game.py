#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy

from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import math
import random
from maze_master.maze import Maze, Direction

def join(elements, separator, last_separator):
  if len(elements) == 0:
    return ""
  output = str(elements[0])
  for i in range(1, len(elements)-1):
    output += separator + str(elements[i])
  if len(elements) > 1:
    output += last_separator + str(elements[len(elements)-1])
  return output

class PlayerNotRegisteredException(Exception):
  pass

class RelativeDirection(Enum):
  Forward = 0
  Right = 1
  Back = 2
  Left = 3

  def __str__(self):
    if self == RelativeDirection.Forward:
      return "forward"
    if self == RelativeDirection.Right:
      return "right"
    if self == RelativeDirection.Back:
      return "back"
    if self == RelativeDirection.Left:
      return "left"

  @staticmethod
  def relative(facing, direction):
    return RelativeDirection((direction.value - facing.value) % 4)

  def absolute(self, facing):
    return Direction((facing.value + self.value) % 4)

class Position:
  def __init__(self, x, y):
    self.X = x
    self.Y = y
  def __eq__(self, another):
    return hasattr(another, 'X') and hasattr(another, 'Y') and self.X == another.X and self.Y == another.Y
  def __ne__(self, another):
    return not self == another
  def __hash__(self):
    return hash(str(self))
  def __repr__(self):
    return f"({self.X},{self.Y})"

class Player:
  def __init__(self, name):
    self.Name = name
    self.position = Position(0,0)
    self.Facing = Direction.North
  def __repr__(self):
    return self.Name

class Location:
  def __init__(self, map_marker, items):
    self.map_marker = map_marker
    self.Items = items

  def __repr__(self):
    return f"{self.map_marker}: {self.Items}"

class Game:
  _free_legend_codes = ["Z", "Y", "X", "W", "V", "U", "T", "S", "R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
  players = {}

  def __init__(self, width, depth):
    self.maze = Maze(width, depth)
    self.start_position = Position(int(width / 2), int(depth / 2))
    self.locations = { self.start_position: Location("0", []) }

  def distance(self, position):
    relativePosition = Position(position.X - self.start_position.X, position.Y - self.start_position.Y)
    return math.sqrt(relativePosition.X * relativePosition.X + relativePosition.Y * relativePosition.Y)

  def pop_free_legend_code(self):
    """Pop a free legend code"""
    if len(self._free_legend_codes) > 0:
      return self._free_legend_codes.pop()
    else:
      return "#"

  def description(self, player):
    output = ""

    if player.position == self.start_position:
      output = "You are facing " + str(player.Facing) + ".\n"

    #add paths
    tile = self.maze.tiles[player.position.X][player.position.Y]
    paths = [RelativeDirection.relative(player.Facing, k) for k in tile.Limits if tile.Limits[k].is_blocked == False]
    if len(paths) > 0:
      output += "\nYou can go " + join(paths, ", ", " or ") + "\n"

    #add items
    if player.position in self.locations:
      itemsText = ""
      for item in self.locations[player.position].Items:
        if item != player:
          itemsText += "\n  - " + str(item)
      if itemsText != "":
        output += "available at location:"
        output += itemsText
    return output

  def add_item(self, position, item):
    if position not in self.locations:
      marker = self._free_legend_codes.pop() if self._free_legend_codes else "#"
      self.locations[position] = Location(marker, [])
    self.locations[position].Items.append(item)

  def remove_item(self, position, item):
    if position not in self.locations:
      return
    self.locations[position].Items.remove(item)
    if position == self.start_position or len(self.locations[position].Items) > 0:
      return
    marker = self.locations[position].map_marker
    del self.locations[position]
    self._free_legend_codes.append(marker)

  def add_player(self, player):
    self.players[player.Name] = player
    player.position = copy.deepcopy(self.start_position)
    self.add_item(player.position, player)

  def remove_player(self, player):
    del self.players[player.Name]
    self.remove_item(player.position, player)

  def move_player(self, player, direction):
    if player.Name not in self.players:
      raise PlayerNotRegisteredException()
    absoluteDirection = direction.absolute(player.Facing)
    tile = self.maze.tiles[player.position.X][player.position.Y]
    limit = tile.limits[absoluteDirection]
    if limit.is_blocked:
      return False
    self.remove_item(player.position, player)
    player.Facing = absoluteDirection
    if absoluteDirection == Direction.North:
      player.position.Y -= 1
    elif absoluteDirection == Direction.East:
      player.position.X += 1
    elif absoluteDirection == Direction.South:
      player.position.Y += 1
    elif absoluteDirection == Direction.West:
      player.position.X -= 1
    self.add_item(player.position, player)
    return True

  def render_legend(self):
    """String text of the legend"""
    text = "\nLEGEND\n"
    for location in self.locations.values():
      text += "  {0}\n".format(location)
    return text

  def render_picture(self, filename):
    """render the maze in a file"""
    monospace = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
    scrap_image = Image.new('RGB', (200, 100))
    pen = ImageDraw.Draw(scrap_image)
    character_size = pen.textsize("0", font=monospace)
    legend = self.render_legend()
    legend_size = pen.textsize(legend, font=monospace)
    corner_size = 4
    character_max_size = max(character_size[0] * 2, character_size[1])
    cell_width = character_max_size + 4
    maze_width = cell_width * self.maze.width + 1
    cell_height = character_max_size + 4
    maze_height = cell_height * self.maze.depth + 1
    image_size_x = max(maze_width, legend_size[0])
    image_size_y = maze_height + legend_size[1]
    image_size = [image_size_x, image_size_y]
    real_image = Image.new('RGB', image_size, (0, 0, 0))
    pen = ImageDraw.Draw(real_image)
    ccell_left = 0
    ccell_top = 0
    for ciy in range(self.maze.depth):
      for cix in range(self.maze.width):
        # TOP
        ccell_right = ccell_left + cell_width
        pen.line((ccell_left, ccell_top + corner_size, ccell_left, ccell_top, ccell_left + corner_size, ccell_top))
        pen.line((ccell_right - corner_size, ccell_top, ccell_right, ccell_top))
        # Bottom
        ccell_bottom = ccell_top + cell_height
        pen.line((ccell_left, ccell_bottom - corner_size, ccell_left, ccell_bottom, ccell_left + corner_size, ccell_bottom))
        pen.line((ccell_right - corner_size, ccell_bottom, ccell_right, ccell_bottom))
        if cix == self.maze.width - 1:
          # Top special
          pen.line((ccell_right, ccell_top, ccell_right, ccell_top + corner_size))
          # Bottom special
          pen.line((ccell_right, ccell_bottom, ccell_right, ccell_bottom - corner_size))
        position = Position(cix, ciy)
        if position in self.locations:
          # Marker
          location = self.locations[position]
          marker = location.map_marker
          marker_x = ccell_left + ((ccell_right - ccell_left) - character_size[0] * len(marker)) / 2
          marker_y = ccell_top + ((ccell_bottom - ccell_top) - character_size[1]) / 2 - 1
          pen.text((marker_x, marker_y), marker, font=monospace, fill=(255, 255, 255))
        # Walls
        tile = self.maze.tiles[cix][ciy]
        if tile.north_limit.is_blocked:
          pen.line((ccell_left + corner_size, ccell_top, ccell_right - corner_size, ccell_top))
        if tile.west_limit.is_blocked:
          pen.line((ccell_left, ccell_top + corner_size, ccell_left, ccell_bottom - corner_size))
        if cix == self.maze.width - 1 and tile.east_limit.is_blocked:
          pen.line((ccell_right, ccell_top + corner_size, ccell_right, ccell_bottom - corner_size))
        if ciy == self.maze.depth - 1 and tile.south_limit.is_blocked:
          pen.line((ccell_left + corner_size, ccell_bottom, ccell_right - corner_size, ccell_bottom))
        # setup for next column
        ccell_left += cell_width
      # setup for next line
      ccell_left = 0
      ccell_top += cell_height

    pen.text((0, maze_height), legend, font=monospace, fill=(255, 255, 255))
    real_image.save(filename)
