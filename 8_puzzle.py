import queue

# To Be Able To Compare Between Two Paths Depending On F-cost Of The Last State In The Path
class Path:
  def __init__(self, list_of_states):
    self.path = list_of_states
  def __lt__(self, other):
    return self.path[-1][0] < other.path[-1][0]

# Add The Puzzle Then Ask For Solve
class Puzzle:
  def __init__(self, initial_state, goal_state):
    self.initial_state = initial_state
    self.goal_state = goal_state

  # To Know If The State Is Solvabel
  def is_solvabel(self):
    inversion = 0
    flat_state = [col for row in self.initial_state for col in row ]
    for i in range(len(flat_state)):
      for j in range(i+1, len(flat_state)):
        if flat_state[i] and flat_state[j] and flat_state[i] > flat_state[j]:
          inversion = inversion + 1
    return True if inversion % 2 == 0 else False

  # Calculate Hamming Distance (H-Cost)
  def hamming_distance(self, current_state):
    return sum(1 for c, g in zip(current_state, self.goal_state) if c != g and c != 0)

  # Calculate Manhattan Distance(H-Cost)
  def manhattan_distance(self, current_state):
    distance = 0
    size = len(current_state)
    for i in range(size):
      for j in range(size):
        tile = current_state[i][j]
        if tile != 0:
          goal_position = self.find_tile_position(tile, self.goal_state)
          distance += abs(i - goal_position[0]) + abs(j - goal_position[1])
    return distance

  # Finding The Index For The Tile
  def find_tile_position(self, tile, state):
    for i, row in enumerate(state):
      for j, value in enumerate(row):
        if value == tile:
          return i, j

  # Generate Available Moves By The Givin State
  def generate_moves(self, current_state):
    moves = []
    empty_position = [(i, row.index(0)) for i, row in enumerate(current_state) if 0 in row][0]

    for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      new_position = (empty_position[0] + move[0], empty_position[1] + move[1])
      # Check If The Move Is Valid (To Not Make It Go Outside The Grid)
      if 0 <= new_position[0] < 3 and 0 <= new_position[1] < 3:
        new_state = [list(row) for row in current_state]
        new_state[empty_position[0]][empty_position[1]], new_state[new_position[0]][new_position[1]] = \
        new_state[new_position[0]][new_position[1]], new_state[empty_position[0]][empty_position[1]]
        moves.append(new_state)
    return moves

  # Simple Function To Check If The Givin State Is The Wanted One
  def is_goal_state(self, current_state):
    return current_state == self.goal_state

  # Solve Using Hamming (Misplaced Tiles)
  def a_star_hamming(self):
    if not self.is_solvabel():
      return [(-1, -1, self.initial_state)]
    priority_queue = queue.PriorityQueue()
    priority_queue.put(Path([(0, 0, self.initial_state)]))  # (f, g, state)
    explored_states = set()
    while not priority_queue.empty():
      path = priority_queue.get().path
      old_g_moves = path[-1][1]
      current_state = path[-1][2]
      if self.is_goal_state(current_state):
        return path
      if tuple(map(tuple,current_state)) in explored_states:
        continue
      explored_states.add(tuple(map(tuple, current_state)))
      for new_state in self.generate_moves(current_state):
        if tuple(map(tuple, new_state)) not in explored_states:
          g_cost = old_g_moves + 1
          h_cost = self.hamming_distance(new_state)
          f_cost = g_cost + h_cost
          new_path = path.copy()
          new_path.append((f_cost, g_cost, new_state))
          priority_queue.put(Path(new_path))

  # Solve Using Manhattan Distance
  def a_star_manhattan(self):
    if not self.is_solvabel():
      return [(-1, -1, self.initial_state)]
    priority_queue = queue.PriorityQueue()
    priority_queue.put(Path([(0, 0, self.initial_state)]))  # (f, moves, state)
    explored_states = set()
    while not priority_queue.empty():
      # current_cost, moves, current_state = priority_queue.get()
      path = priority_queue.get().path
      old_g_cost = path[-1][1]
      current_state = path[-1][2]
      if self.is_goal_state(current_state):
        return path
      if tuple(map(tuple, current_state)) in explored_states:
        continue
      explored_states.add(tuple(map(tuple, current_state)))
      for new_state in self.generate_moves(current_state):
        if tuple(map(tuple, new_state)) not in explored_states:
          g_cost = old_g_cost + 1
          h_cost = self.manhattan_distance(new_state)
          f_cost = g_cost + h_cost
          new_path = path.copy()
          new_path.append((f_cost, g_cost, new_state))
          priority_queue.put(Path(new_path))

# Example usage:
initial_state = [
  [1, 2, 3],
  [5, 6, 0],
  [7, 8, 4]
  # [3, 8, 6],
  # [5, 0, 4],
  # [7, 2, 1]
]
# 18
goal_state = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 0]
]

puzzle_hamming = Puzzle(initial_state, goal_state)
puzzle_manhatan = Puzzle(initial_state, goal_state)
# A* using Hamming distance
path1 = puzzle_hamming.a_star_hamming()
# A* using Manhatan distance
path2 = puzzle_manhatan.a_star_manhattan()

if(path1[0][0] == -1):
  print("This State Is Not Solvabe Try Another One.")
else:
  print("Moves Using Misplaced Tiles Heuristic: ")
  for i in range(len(path1)):
    if i > 0:
      print("Move {0}: ".format(i))
      f, g, state = path1[i]
      for row in state:
        for col in row:
          print(col, end=" ")
        print("")
      print("\n\n")

  print("############")

  print("Moves Manhattan Distance Heuristic: ")
  for i in range(len(path2)):
    if i > 0:
      print("Move {0}: ".format(i))
      f, g, state = path2[i]
      for row in state:
        for col in row:
          print(col, end=" ")
        print("")
      print("\n\n")