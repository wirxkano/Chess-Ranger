import sys
from constants import *
from data import *
from gui import *
from solver import *
import random

def printUsage():
  print("To use BrFS algorithm run command: python main.py 0")
  print("To use BFS algorithm run command: python main.py 1")

def chess_label(pos):
  row, col = pos
  letters = 'abcdefgh'
  numbers = '12345678'
  column_label = letters[col]
  row_label = numbers[7 - row]
  
  return f"{row_label}{column_label}"

def main(argv):
  if len(argv) < 1:
    printUsage()
  else:
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess Ranger")
    clock = p.time.Clock()
    screen.fill("black")
    font = p.font.Font('freesansbold.ttf', 12)
    
    init_state = init_states[random.randint(0, len(init_states) - 1)]
    # init_state = init_states[9]
    
    print("Press space to find next step, press 'N' to start new game!")
    
    gui = GUI(init_state)
    solver = Solver()
    
    solution = None
    mode = argv[0]
    
    if mode == '0':
      solution = solver.brfs(init_state)
    elif mode == '1':
      solution = solver.bfs(init_state)
    else:
      printUsage()
      return
  
    current_step = 0
    running = True
    
    while running:
      for event in p.event.get():
        if event.type == p.QUIT:
          running = False
                  
        elif event.type == p.KEYDOWN:
          if len(solution) == 0:
              print("No solution! Please press 'N' to start new game")
          
          if event.key == p.K_SPACE and current_step < len(solution):
            from_pos, to_pos = solution[current_step]
            print(chess_label(from_pos), '->', chess_label(to_pos))
            solver.make_move(init_state, from_pos, to_pos)
            current_step += 1
            
          if event.key == p.K_n:
            print('--------------------------- NEW GAME ---------------------------')
            init_state = init_states[random.randint(0, len(init_states) - 1)]
            if mode == '0':
              solution = solver.brfs(init_state)
            elif mode == '1':
              solution = solver.bfs(init_state)
            current_step = 0
            gui = GUI(init_state)

        # RENDER GAME
        gui.load_images()
        gui.draw_board(screen)
        gui.draw_pieces(screen)
        gui.draw_labels(screen, font)
        p.display.flip()

        clock.tick(60)

if __name__ == '__main__':
  main(sys.argv[1:])