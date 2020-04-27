from random import shuffle
import math

from problem import Problem
import maze

class PacManProblem(Problem):
    index_by = lambda ij, m: m[ij[0]][ij[1]]

    """
    Parameters
      initial : (int, int)
        pacman's initial postition at the map
      goal : (int, int)
        goal postition at the maze
      maze : [[char]]
        matrix representing the maze, where the cell's values represent:
          0 - free position
         -2 - ghosts
         -1 - wall
          1 - COIN
          S - pacman's initial (start) position
          F - pacman's target (goal) position
    """
    def __init__(self, initial, goal, maze_map, shuffle_actions_list=False):
        assert(index_by(initial, maze_map) == maze.START)
        assert(index_by(goal, maze_map) == maze.GOAL)

        Problem.__init__(self, self.initial, self.goal)
        self.maze = maze_map
        self.height = len(maze_map)
        self.width = len(maze_map[0])
        self.shuffle_actions_list = shuffle_actions_list

    def __is_valid_pos(self, pos):
        i, j = pos
        return  (0 <= i and i < self.height and
                0 <= j and j < self.width and
                self.maze[i][j] != maze.GHOST and
                self.maze[i][j] != maze.WALL)

    def __is_valid_move(self, from_pos, to_pos):
        from_i, from_j = from_pos
        to_i, to_j = to_pos

        delta = abs((from_i-to_i) + (from_j-to_j))
        return (self.__is_valid_pos(from_pos) and
               self.__is_valid_pos(to_pos) and
               delta <= 1)

    """
    Parameters
      state : (int, int)
        pacman's current postition at the maze
    """
    def actions(self, state):
        directions = [(-1,0), (0,1), (1,0), (0,-1)] #left, top, right, bottom

        i, j = state
        actions_list = [(i + di, j + dj) for (di, dj) in directions]

        if (self.shuffle_actions_list):
            shuffle(actions_list) # randomizes actions' order

        return [pos for pos in actions_list if self.__is_valid_move(state, pos)]

    """
    Parameters
      state : (int, int)
        pacman's current postition at the maze
      action : (int, int)
        position the pacman will move to
    """
    def result(self, state, action):
        return action # assumed to be a valid action in the state

    """
    Parameters
      state : (int, int)
        pacman's current postition at the maze
    """
    def goal_test(self, state):
        return state == self.goal

    """
    Parameters
      cost_so_far : int
        cost already paid to get to current state
      current_pos : (int, int)
        pacman's current postition at the maze
      action : (int, int)
        position the pacman would move to
      next_pos : (int, int)
        pacman's next postition at the maze
    """
    def path_cost(self, cost_so_far, current_pos, action, next_pos):
        if action == next_pos and self.__valid_move(current_pos, next_pos):
            return cost_so_far + 1

        return math.inf

    """
    Parameters
      state : (int, int)
        pacman's current postition at the maze
        for which we estimate the lowest path cost to the goal
    """
    def h(self, state):
        return manhattan(state, goal)

    """
    Parameters
      state : (int, int)
        pacman's current postition at the maze

    This acts as a bit of extra information in problems where we try to
    optimise a value when we cannot do a goal test. Used in Hill-climbing algorithm.
    """
    def value(self, state):
        i, j = state

        if self.maze[i][j] == maze.FREE:
            return 1

        if self.maze[i][j] == maze.COIN:
            return 2

        return -math.inf