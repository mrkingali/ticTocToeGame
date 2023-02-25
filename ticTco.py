import pygame as pg
import sys
from random import randint

vec2 = pg.math.Vector2

# size of our object
WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE // 3
CELL_CENTER = vec2(CELL_SIZE / 2)

# picture path
FIELD_PICTURE = 'pic/field.PNG'
O_PICTURE = 'pic/O.PNG'
X_PICTURE = 'pic/X.PNG'

# declare infinity number
INF = float('inf')

# core of our game
class ticTocGame:
    """
    its our initial function
    you can know the variable by their name
    """
    def __init__(self, game):
        self.game = game
        self.fieldImage = self.getScaledImage(FIELD_PICTURE, [WINDOW_SIZE, WINDOW_SIZE])
        self.oImage = self.getScaledImage(O_PICTURE, [CELL_SIZE - 50] * 2)
        self.xImage = self.getScaledImage(X_PICTURE, [CELL_SIZE - 50] * 2)
        self.gameArray = [[INF, INF, INF],
                          [INF, INF, INF],
                          [INF, INF, INF]]
        self.player = randint(0, 1)
        self.winner = None
        self.gameStep = 0
        """ 
        imposible line that would creat by player 1 or 0
        """
        self.lineIndicesArray = [[(0, 0), (0, 1), (0, 2)],
                                 [(1, 0), (1, 1), (1, 2)],
                                 [(2, 0), (2, 1), (2, 2)],
                                 [(0, 0), (1, 0), (2, 0)],
                                 [(0, 1), (1, 1), (2, 1)],
                                 [(0, 2), (1, 2), (2, 2)],
                                 [(0, 0), (1, 1), (2, 2)],
                                 [(2, 0), (1, 1), (0, 2)], ]

    """
    this function get the image from sourse
    then resize that to correct size then return it
    """
    @staticmethod
    def getScaledImage(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    """
    this function every time chek that if there is an winner
    """
    def chekWinner(self):
        for line in self.lineIndicesArray:
            sumLine = sum([self.gameArray[i][j] for i, j in line])
            if sumLine in {0, 3}:
                self.winner = 'XO'[sumLine == 0]
                self.winnerLine = [vec2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                   vec2(line[2][::-1]) * CELL_SIZE + CELL_CENTER]

    """
    if it fine winner this function gonna print the line
    """
    def drawWinner(self):
        if self.winner:
            pg.draw.line(self.game.screen, "red", *self.winnerLine, CELL_SIZE // 8)

    """
    this function gonna draw X and O in game
    """
    def drawObject(self):
        for Y, row in enumerate(self.gameArray):
            for X, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.xImage if obj else self.oImage, vec2(X, Y) * CELL_SIZE)

    """
    this function listen to the mouse click
    if it pressed set X and O in their place
    """
    def runGameProcess(self):
        currentCell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, currentCell)
        leftClick = pg.mouse.get_pressed()[0]
        if leftClick and self.gameArray[row][col] == INF and not self.winner:
            self.gameArray[row][col] = self.player
            self.player = not self.player
            self.gameStep += 1
            self.chekWinner()

    """ 
    this is ganna draw all the object in game
    """
    def draw(self):
        self.game.screen.blit(self.fieldImage, (0, 0))
        self.drawObject()
        self.drawWinner()

    """
    use to print caption for user on top of the window
    """
    def printCaption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'congratulation Player "{"OX"[self.player]}" had won the game')

    """
    run the game
    """
    def start(self):
        self.draw()
        self.runGameProcess()
        self.printCaption()

# our game class
class Game:

    """
    set the window for game
    """
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WINDOW_SIZE, WINDOW_SIZE])
        self.time = pg.time.Clock()
        self.tictok = ticTocGame(self)

    def newGame(self):
        self.tictok = ticTocGame(self)

    """
    to listen and control the button on window and keyboar
    """
    def chekGame(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.newGame()

    """
    would run the game
    """
    def start(self):
        while (True):
            self.tictok.start()
            self.chekGame()
            pg.display.update()
            self.time.tick(60)


if __name__ == '__main__':
    game = Game()
    game.start()
