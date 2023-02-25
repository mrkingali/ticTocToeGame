import pygame as pg
import sys
from random import randint
vec2 = pg.math.Vector2
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3
CELL_CENTER=vec2(CELL_SIZE/2)
FIELD_PICTURE = 'pic/field.PNG'
O_PICTURE = 'pic/O.PNG'
X_PICTURE = 'pic/X.PNG'

INF = float('inf')



class ticTocGame:
    def __init__(self, game):
        self.game = game
        self.fieldImage = self.getScaledImage(FIELD_PICTURE, [WINDOW_SIZE, WINDOW_SIZE])
        self.oImage = self.getScaledImage(O_PICTURE, [CELL_SIZE - 50] * 2)
        self.xImage = self.getScaledImage(X_PICTURE, [CELL_SIZE - 50] * 2)
        self.gameArray = [[INF, INF, INF],
                          [INF, INF, INF],
                          [INF, INF, INF]]
        self.player = randint(0, 1)

        self.lineIndicesArray = [[(0, 0), (0, 1), (0, 2)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],

                                 [(0, 0), (1, 0), (2, 0)],
                                 [(0, 1), (1, 1), (2, 1)],
                                 [(0, 2), (1, 2), (2, 2)],

                                 [(0, 0), (1, 1), (2, 2)],
                                 [(2, 0), (1, 1), (0, 2)],

                                 ]

        self.winner=None
        self.gameStep=0
    def chekWinner(self):
        for line in self.lineIndicesArray:
            sumLine=sum([self.gameArray[i][j] for i,j in line])

            if sumLine in {0,3}:
                self.winner='XO'[sumLine==0]
                self.winnerLine=[vec2(line[0][::-1])*CELL_SIZE+CELL_CENTER,
                                 vec2(line[2][::-1])*CELL_SIZE+CELL_CENTER]

    def drawWinner(self):
        if self.winner:
            pg.draw.line(self.game.screen,"red",*self.winnerLine,CELL_SIZE//8)

    def drawObject(self):
        for Y, row in enumerate(self.gameArray):
            for X, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.xImage if obj else self.oImage, vec2(X, Y) * CELL_SIZE)

    def runGameProcess(self):
        currentCell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, currentCell)
        leftClick = pg.mouse.get_pressed()[0]
        if leftClick and self.gameArray[row][col] == INF and not self.winner:
            self.gameArray[row][col] = self.player
            self.player = not self.player
            self.gameStep+=1
            self.chekWinner()
    def draw(self):
        self.game.screen.blit(self.fieldImage, (0, 0))
        self.drawObject()
        self.drawWinner()

    @staticmethod
    def getScaledImage(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def printCaption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'congratulation Player "{"OX"[self.player]}" had won the game')
    def start(self):
        self.draw()
        self.runGameProcess()
        self.printCaption()


class Game:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
        self.time = pg.time.Clock()
        self.tictok = ticTocGame(self)

    def newGame(self):
        self.tictok=ticTocGame(self)

    def chekWinner(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    self.newGame()

    def start(self):
        while (True):
            self.tictok.start()
            self.chekWinner()
            pg.display.update()
            self.time.tick(60)


if __name__ == '__main__':
    game = Game()
    game.start()
