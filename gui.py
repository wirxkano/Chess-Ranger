import pygame as p
from constants import *

class GUI:
  def __init__(self, state):
    self.state = state
    
  def load_images(self):
    pieces = ['bb', 'bk', 'bn', 'bp', 'bq', 'br', 'wb', 'wk', 'wn', 'wp', 'wq', 'wr']
    for piece in pieces:
      IMAGES[piece] = p.transform.scale(p.image.load('images/' + piece + '.png'), (CELL_SZ, CELL_SZ))
  
  def draw_board(self, screen):
    cnt = 0
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if cnt % 2 == 0:
                p.draw.rect(screen, p.Color(240, 217, 181),[CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
            else:
                p.draw.rect(screen, p.Color(181, 136, 99), [CELL_SZ * j, CELL_SZ * i, CELL_SZ, CELL_SZ])
            cnt +=1

        cnt-=1
  
  def draw_pieces(self, screen):
    for i in range(DIMENSION):
      for j in range(DIMENSION):
        piece = self.state[i][j]
        if piece != '--':
          screen.blit(IMAGES[piece], p.Rect(j * CELL_SZ, i * CELL_SZ, CELL_SZ, CELL_SZ))
          
  def draw_labels(self, screen, font):
    letters = 'abcdefgh'
    numbers = '12345678'

    for col in range(DIMENSION):
        text = font.render(letters[col], True, p.Color('black'))
        x = col * CELL_SZ + CELL_SZ // 2 - text.get_width() // 2
        y = HEIGHT - text.get_height()
        screen.blit(text, (x, y))

    for row in range(DIMENSION):
        text = font.render(numbers[7 - row], True, p.Color('black'))
        x = WIDTH - text.get_width()
        y = row * CELL_SZ + CELL_SZ // 2 - text.get_height() // 2
        screen.blit(text, (x, y))
