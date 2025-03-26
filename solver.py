from constants import *
from collections import deque
import heapq
from memory_profiler import memory_usage
import time

class Solver:
  def __init__(self):
    self.step = 0
  
  def rules(self, piece):
    directions = []
    
    if piece in ['wp']: # White Pawn
      directions = [(-1, -1), (-1, 1)]
      
    elif piece in ['bp']: # Black Pawn
      directions = [(1, -1), (1, 1)]
      
    elif piece in ['wb', 'bb']:  # Bishop
      directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
      
    elif piece in ['wn', 'bn']: # Knight
      directions = [
        (-1, 2), (-2, 1), (1, 2), (2, 1),
        (-1, -2), (-2, -1), (1, -2), (2, -1)
      ]
      
    elif piece in ['wr', 'br']:  # Rook
      directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
      
    elif piece in ['wk', 'bk', 'wq', 'bq']:  # King, Queen
      directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0),   (1, 1)
      ]
      
    return directions
  
  def is_goal_state(self, state):
    pieces = sum(row.count(piece) for row in state for piece in row if piece != '--')
    
    return pieces == 1
  
  def get_piece_move(self, state, r, c):
    piece = state[r][c]
    moves = []
    
    if piece == '--':
      return moves
    directions = self.rules(piece)
        
    for dr, dc in directions:
      new_r, new_c = dr + r, dc + c
      while 0 <= new_r < DIMENSION and 0 <= new_c < DIMENSION:
        if state[new_r][new_c] != '--':
          moves.append((new_r, new_c))
          break
        
        if piece in ['wk', 'bk', 'wp', 'bp', 'wn', 'bn']:
          break
        
        new_r += dr
        new_c += dc
        
    return moves
        
  def get_all_moves(self, state):
    all_moves = []
    for r in range(DIMENSION):
      for c in range(DIMENSION):
        if state[r][c] != '--':
          for move in self.get_piece_move(state, r, c):
            all_moves.append(((r, c), move))
          
    return all_moves
  
  def make_move(self, state, from_pos, to_pos):
    r1, c1 = from_pos
    r2, c2 = to_pos
    state[r2][c2] = state[r1][c1]
    state[r1][c1] = '--'
    
    return state
  
  def brfs(self, init_state):
    start_time = time.time()
    mem_usage_before = memory_usage()[0]
    q = deque([(init_state, [])])
    visited = set()
    self.step = 0
    
    while q:
      current_state, path = q.popleft()
      adj_state = tuple(tuple(row) for row in current_state)
      
      if adj_state in visited:
        continue
      
      visited.add(adj_state)
      
      if self.is_goal_state(current_state):
        end_time = time.time()
        mem_usage_after = memory_usage()[0]

        execution_time = end_time - start_time
        mem_usage = mem_usage_after - mem_usage_before
        print(f"Execution time: {execution_time} seconds")
        print(f"Number of steps: {self.step}")
        print(f"Memory usage: {mem_usage} MiB")
        return path
      
      for move in self.get_all_moves(current_state):
        from_pos, to_pos = move
        new_state = [row[:] for row in current_state]
        self.make_move(new_state, from_pos, to_pos)
        q.append((new_state, path + [move]))
        
      self.step += 1
        
    return []
  
  def heuristic(self, state):
    num_pieces = sum(row.count(piece) for row in state for piece in row if piece != '--')
    if num_pieces == 1:
        return 0

    piece_positions = [(r, c) for r in range(DIMENSION) for c in range(DIMENSION) if state[r][c] != '--']
    total_distance = sum(abs(r1 - r2) + abs(c1 - c2) for i, (r1, c1) in enumerate(piece_positions)
                         for r2, c2 in piece_positions[i+1:])
    
    return num_pieces + total_distance / (num_pieces + 1)
    
  def bfs(self, init_state):
    start_time = time.time()
    mem_usage_before = memory_usage()[0]
    open_list = []
    close_list = set()
    self.step = 0
    
    heapq.heappush(open_list, (self.heuristic(init_state), [], init_state))
    
    while open_list:
      _, path, current_state = heapq.heappop(open_list)
      
      if self.is_goal_state(current_state):
        end_time = time.time()
        mem_usage_after = memory_usage()[0]

        execution_time = end_time - start_time
        mem_usage = mem_usage_after - mem_usage_before
        print(f"Execution time: {execution_time} seconds")
        print(f"Number of steps: {self.step}")
        print(f"Memory usage: {mem_usage} MiB")
        return path
      
      adj_state = tuple(tuple(row) for row in current_state)
      if adj_state in close_list:
        continue
      
      close_list.add(adj_state)
      
      for move in self.get_all_moves(current_state):
        from_pos, to_pos = move
        new_state = [row[:] for row in current_state]
        self.make_move(new_state, from_pos, to_pos)
        heapq.heappush(open_list, (self.heuristic(new_state), path + [(from_pos, to_pos)], new_state))
      
      self.step += 1
  
    return []
    
    