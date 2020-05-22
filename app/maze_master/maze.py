''' MAZE class '''
from enum import Enum
import random

class Direction(Enum):
  '''Absolute direction enumeration'''
  North = 0
  East = 1
  South = 2
  West = 3

  def __str__(self):
    if self == Direction.North:
      return 'north'
    if self == Direction.East:
      return 'east'
    if self == Direction.South:
      return 'south'
    if self == Direction.West:
      return 'west'

  def invert(self):
    '''Inverts the direction'''
    return Direction((self.value + 2) % 4)

class Limit:
  '''Represents a limit of a maze tile.'''
  def __init__(self):
    self.is_blocked = True

class Tile:
  '''Represent a tile of the Maze'''
  def __init__(self, x, y, northLimit, eastLimit, southLimit, westLimit):
    self.position_x = x
    self.position_y = y
    self.limits = {Direction.North: northLimit, Direction.East: eastLimit, Direction.South: southLimit, Direction.West: westLimit}
    self.north_limit = northLimit
    self.east_limit = eastLimit
    self.south_limit = southLimit
    self.west_limit = westLimit

  def is_all_blocked(self):
    '''Return true if all limits are blocked'''
    return self.north_limit.is_blocked and self.east_limit.is_blocked and self.south_limit.is_blocked and self.west_limit.is_blocked

class Maze:
  '''The maze'''
  def __init__(self, width, depth):
    self.width = width
    self.depth = depth
    width_limits = [[Limit() for y in range(depth + 1)] for x in range(width + 1)]
    depth_limits = [[Limit() for y in range(depth + 1)] for x in range(width + 1)]
    self.tiles = [[Tile(x, y, depth_limits[x][y], width_limits[x+1][y], depth_limits[x][y+1], width_limits[x][y]) for y in range(depth)] for x in range(width)]
    
    #Algorithm
    # set TotalCells = number of cells in grid
    total_tiles_count = width * depth
    # set VisitedCells = 1
    visited_tile_count = 1

    # choose a cell at 'random' and call it CurrentCell
    current_tile = self.tiles[random.randint(0, width-1)][random.randint(0, depth-1)]
    # create a track (LIFO) to hold the path made while moving in the maze
    track = [current_tile]

    while visited_tile_count < total_tiles_count:
      # Find all neighbors of CurrentCell with all walls intact
      unvisited_directions = []
      west_neighbor = None
      if current_tile.position_x > 0:
        west_neighbor = self.tiles[current_tile.position_x-1][current_tile.position_y]
        if west_neighbor.is_all_blocked():
          unvisited_directions.append(Direction.West)
      north_neighbor = None
      if current_tile.position_y > 0:
        north_neighbor = self.tiles[current_tile.position_x][current_tile.position_y-1]
        if north_neighbor.is_all_blocked():
          unvisited_directions.append(Direction.North)
      east_neighbor = None
      if current_tile.position_x < width - 1:
        east_neighbor = self.tiles[current_tile.position_x+1][current_tile.position_y]
        if east_neighbor.is_all_blocked():
          unvisited_directions.append(Direction.East)
      south_neighbor = None
      if current_tile.position_y < depth - 1:
        south_neighbor = self.tiles[current_tile.position_x][current_tile.position_y+1]
        if south_neighbor.is_all_blocked():
          unvisited_directions.append(Direction.South)

      # If one or more found
      if unvisited_directions:
        # Push current tile on the CellStack
        track.append(current_tile)
        # Choose one at random
        direction = random.choice(unvisited_directions)
        # Knock down the wall between it and CurrentCell
        if direction == Direction.West:
          current_tile.west_limit.is_blocked = False
          # Make the new tile the current tile
          current_tile = west_neighbor
        elif direction == Direction.North:
          current_tile.north_limit.is_blocked = False
          # Make the new tile the current tile
          current_tile = north_neighbor
        elif direction == Direction.East:
          current_tile.east_limit.is_blocked = False
          # Make the new tile the current tile
          current_tile = east_neighbor
        elif direction == Direction.South:
          current_tile.south_limit.is_blocked = False
          # Make the new tile the current tile
          current_tile = south_neighbor
        # increment visited tile count
        visited_tile_count += 1
      else:
        # Pop the most recent cell entry off the CellStack and make it CurrentCell
        current_tile = track.pop()
