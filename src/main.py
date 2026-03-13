import pygame
import random

TILE_EMPTY = 0
TILE_CROSS = 1
TILE_CIRCLE = 2

TURN_NONE = 0
TURN_X = 1
TURN_O = 2
TURN_X_WON = 3
TURN_O_WON = 4
TURN_DRAW = 5

class TicTacToe:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        self.running = True
        self.turn = TURN_X
        self.field = [
            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ],
            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ],
            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ]
        ]
        self.breiteZelle = 1.0 / 3 
        self.hoeheZelle = 1.0 / 3  

    def __deinit__(self):
        pygame.quit()

    def draw_title(self, text):
        bitmap = self.font.render(str(text), True, (0, 255, 0))
        self.screen.blit(bitmap, ((self.WIDTH - bitmap.width) / 2, (self.HEIGHT - bitmap.height) / 2))
    
    def draw_cross(self, x, y, w, h):
        pygame.draw.aaline(self.screen, "white", (self.WIDTH * x, self.HEIGHT * y),        (self.WIDTH * (x + w), self.HEIGHT * (y + h)), 20)
        pygame.draw.aaline(self.screen, "white", (self.WIDTH * x, self.HEIGHT * (y + h)), (self.WIDTH * (x + w), self.HEIGHT * y       ), 20)

    def draw_circle(self, x, y, w, h):
        pygame.draw.ellipse(self.screen, "white", (self.WIDTH * x, self.HEIGHT * y, self.WIDTH * w, self.HEIGHT * h), 20)

    def tile_won(self, tile):
        return (
            (self.field[0][0] == tile and self.field[0][1] == tile and self.field[0][2] == tile) or
            (self.field[1][0] == tile and self.field[1][1] == tile and self.field[1][2] == tile) or
            (self.field[2][0] == tile and self.field[2][1] == tile and self.field[2][2] == tile) or
            (self.field[0][0] == tile and self.field[1][0] == tile and self.field[2][0] == tile) or
            (self.field[0][1] == tile and self.field[1][1] == tile and self.field[2][1] == tile) or
            (self.field[0][2] == tile and self.field[1][2] == tile and self.field[2][2] == tile) or
            (self.field[0][0] == tile and self.field[1][1] == tile and self.field[2][2] == tile) or
            (self.field[2][0] == tile and self.field[1][1] == tile and self.field[0][2] == tile)
        )

    def player_won(self) -> int:
        if self.tile_won(TILE_CROSS):
            return TURN_X_WON
        elif self.tile_won(TILE_CIRCLE):
            return TURN_O_WON
        else:
            return TURN_NONE

    def field_set(self, x, y, tile):
        self.field[y][x] = tile
        winner = self.player_won()
        if winner != TURN_NONE:
            self.turn = winner
            return 
    
        for y in range(0, 3):
            for x in range(0, 3):
                if self.field[y][x] == TILE_EMPTY:
                    return
                
        self.turn = TURN_DRAW

    def field_empty(self, x, y):
        return self.field[y][x] == TILE_EMPTY

    def player_click(self):
        if pygame.mouse.get_just_pressed()[0]:
            pos = pygame.mouse.get_pos()

            tx = int(pos[0] / self.WIDTH * 3)
            ty = int(pos[1] / self.HEIGHT * 3)
    
            if self.field_empty(tx,ty) and self.turn == TURN_O:
                self.turn = TURN_X
                self.field_set(tx, ty, TILE_CIRCLE)
            elif self.field_empty(tx,ty) and self.turn == TURN_X:
                self.turn = TURN_O
                self.field_set(tx, ty, TILE_CROSS)

    def x_fill(self, y, tile) -> int:
        if self.field[y][0] == TILE_EMPTY and self.field[y][1] == tile and self.field[y][2] == tile:
            return 0
        elif self.field[y][0] == tile and self.field[y][1] == TILE_EMPTY and self.field[y][2] == tile:
            return 1
        elif self.field[y][0] == tile and self.field[y][1] == tile and self.field[y][2] == TILE_EMPTY:
            return 2
        else:
            return -1
    
    def y_fill(self, x, tile) -> int:
        if self.field[0][x] == TILE_EMPTY and self.field[1][x] == tile and self.field[2][x] == tile:
            return 0
        elif self.field[0][x] == tile and self.field[1][x] == TILE_EMPTY and self.field[2][x] == tile:
            return 1
        elif self.field[0][x] == tile and self.field[1][x] == tile and self.field[2][x] == TILE_EMPTY:
            return 2
        else:
            return -1
            
    def diagonal_fill(self, tile):
        if self.field[0][0] == TILE_EMPTY and self.field[1][1] == tile and self.field[2][2] == tile:
            return [0,0]
        elif self.field[0][0] == tile and self.field[1][1] == TILE_EMPTY and self.field[2][2] == tile:
            return [1,1]
        elif self.field[0][0] == tile and self.field[1][1] == tile and self.field[2][2] == TILE_EMPTY:
            return [2,2]
        elif self.field[0][2] == TILE_EMPTY and self.field[1][1] == tile and self.field[2][0] == tile:
            return [0,2]
        elif self.field[0][2] == tile and self.field[1][1] == TILE_EMPTY and self.field[2][0] == tile:
            return [1,1]
        elif self.field[0][2] == tile and self.field[1][1] == tile and self.field[2][0] == TILE_EMPTY:
            return [2,0]
        else:
            return []
        
    def player_bot(self):
        if self.turn == TURN_O:
            self.turn = TURN_X
            
            if (xindex := self.x_fill(0,TILE_CIRCLE)) >= 0:
                self.field_set(xindex, 0, TILE_CIRCLE)
            elif (xindex := self.x_fill(1,TILE_CIRCLE)) >= 0:
                self.field_set(xindex, 1, TILE_CIRCLE)
            elif (xindex := self.x_fill(2,TILE_CIRCLE)) >= 0:
                self.field_set(xindex, 2, TILE_CIRCLE)
            elif (xindex := self.x_fill(0,TILE_CROSS)) >= 0:
                self.field_set(xindex, 0, TILE_CIRCLE)
            elif (xindex := self.x_fill(1,TILE_CROSS)) >= 0:
                self.field_set(xindex, 1, TILE_CIRCLE)
            elif (xindex := self.x_fill(2,TILE_CROSS)) >= 0:    
                self.field_set(xindex, 2, TILE_CIRCLE)
            elif (yindex := self.y_fill(0,TILE_CIRCLE)) >= 0:
                self.field_set(0, yindex, TILE_CIRCLE)
            elif (yindex := self.y_fill(1,TILE_CIRCLE)) >= 0:
                self.field_set(1, yindex, TILE_CIRCLE)
            elif (yindex := self.y_fill(2,TILE_CIRCLE)) >= 0:
                self.field_set(2, yindex, TILE_CIRCLE)
            elif (yindex := self.y_fill(0,TILE_CROSS)) >= 0:
                self.field_set(0, yindex, TILE_CIRCLE)
            elif (yindex := self.y_fill(1,TILE_CROSS)) >= 0:
                self.field_set(1, yindex, TILE_CIRCLE)
            elif (yindex := self.y_fill(2,TILE_CROSS)) >= 0:
                self.field_set(2, yindex, TILE_CIRCLE)
            elif (xyindex := self.diagonal_fill(TILE_CIRCLE)) != []:
                self.field_set(xyindex[0], xyindex[1], TILE_CIRCLE)
            elif (xyindex := self.diagonal_fill(TILE_CROSS)) != []:
                self.field_set(xyindex[0], xyindex[1], TILE_CIRCLE)
            else:
                for i in range(0,1000):
                    tx = random.randint(0, 2)
                    ty = random.randint(0, 2)
                    if self.field_empty(tx, ty):
                        self.field_set(tx, ty, TILE_CIRCLE)
                        return
                self.turn = TURN_DRAW

    def render(self):
        BOARD_SIZE = min(self.WIDTH, self.HEIGHT)

        self.player_click()
        self.player_bot()
        
        if self.turn == TURN_X_WON:
            self.screen.fill("red")
        elif self.turn == TURN_O_WON:
            self.screen.fill("blue")
        elif self.turn == TURN_DRAW:
            self.screen.fill("grey")
        else:
            self.screen.fill("black")

        for y in range(0, 3):
            for x in range(0, 3):
                if self.field[y][x] == TILE_CROSS:
                    self.draw_cross((x+1) * self.breiteZelle - 0.3, (y+1) * self.hoeheZelle - 0.3, self.breiteZelle * 0.75, self.hoeheZelle * 0.75)
        
        for y in range(0, 3):
            for x in range(0, 3):
                if self.field[y][x] == TILE_CIRCLE:
                    self.draw_circle((x+1) * self.breiteZelle - 0.3, (y+1) * self.hoeheZelle - 0.3, self.breiteZelle * 0.75, self.hoeheZelle * 0.75)
        
        pygame.draw.aaline(self.screen, "white", (BOARD_SIZE*(1/3), BOARD_SIZE*0), (BOARD_SIZE*(1/3), BOARD_SIZE*1), 20)
        pygame.draw.aaline(self.screen, "white", (BOARD_SIZE*(2/3), BOARD_SIZE*0), (BOARD_SIZE*(2/3), BOARD_SIZE*1), 20)
        pygame.draw.aaline(self.screen, "white", (BOARD_SIZE*0, BOARD_SIZE*(1/3)), (BOARD_SIZE*1, BOARD_SIZE*(1/3)), 20)
        pygame.draw.aaline(self.screen, "white", (BOARD_SIZE*0, BOARD_SIZE*(2/3)), (BOARD_SIZE*1, BOARD_SIZE*(2/3)), 20)

        font = pygame.font.Font(None,150)
        
        if self.turn == TURN_X_WON:
            text = font.render("X is the Winner",True,(0,0,0))
            self.screen.blit(text, (150, 400))
        elif self.turn == TURN_O_WON:
            text = font.render("O is the Winner",True,(0,0,0))
            self.screen.blit(text, (150, 400))
        elif self.turn == TURN_DRAW:
            text = font.render("It's a Draw",True,(0,0,0))
            self.screen.blit(text, (250, 400))
        

    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    self.WIDTH, self.HEIGHT = event.w, event.h
                    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.turn = TURN_X
                        self.field = [
                            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ],
                            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ],
                            [ TILE_EMPTY, TILE_EMPTY, TILE_EMPTY ]
                        ]
            
            self.render()
            pygame.display.flip()
            self.clock.tick(60)


ttt = TicTacToe()
ttt.main()
ttt.__deinit__()