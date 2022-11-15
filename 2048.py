import tempfile
import pygame
from random import randint
from copy import deepcopy

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

#       x  y
GRID = [7, 7]
BOX_HEIGHT = 100
SCREEN_HEIGHT = GRID[0]*BOX_HEIGHT
SCREEN_WIDTH = GRID[1]*BOX_HEIGHT

SCREEN_DIMENSIONS = [SCREEN_HEIGHT, SCREEN_WIDTH]

def pullUpRecursion(tempMatrix):
    matrixCopy = deepcopy(tempMatrix)
    for y in range(len(tempMatrix)):
        for x in range(len(tempMatrix[0])):    
            if y < len(tempMatrix)-1:
                # check if merging possible
                if tempMatrix[y][x] == tempMatrix[y+1][x] and tempMatrix[y][x] != 0:
                    tempMatrix[y][x] = tempMatrix[y+1][x]*2
                    tempMatrix[y+1][x] = 0
                
                # otherwise pull up
                elif tempMatrix[y][x] == 0 and tempMatrix[y+1][x] != 0:
                    tempMatrix[y][x] = tempMatrix[y+1][x]
                    tempMatrix[y+1][x] = 0
                    # print('pull')

    if tempMatrix != matrixCopy:
        tempMatrix = pullUpRecursion(tempMatrix)

    return tempMatrix



def pullUp(inputMatrix):
    pulledMatrix = pullUpRecursion(inputMatrix)
    rand_x, rand_y = randint(0,len(pulledMatrix[0])-1),randint(0,len(pulledMatrix)-1) 
    if pulledMatrix[rand_y][rand_x] == 0:
        pulledMatrix[rand_y][rand_x] = 4 if randint(1,10) == 4 else 2
    else:
        pullUp(pulledMatrix)
    return pulledMatrix


def rotateMatrixClock(inputMatrix):
    return tupleMatrixToMatrix(list(zip(*inputMatrix[::-1])))

def rotateMatrixAnticlock(inputMatrix):
    return tupleMatrixToMatrix(list(zip(*inputMatrix)))[::-1]

def tupleMatrixToMatrix(inputMatrix):
    return [list(element) for element in inputMatrix]

def matrixLineBreakString(inputMatrix):
    print_string = ''
    for i in range(len(inputMatrix)-1):
        print_string += '\t' + str(inputMatrix[i]) + '\n'
    print_string += '\t' + str(inputMatrix[-1])
    return print_string + '\n'

class GameMatrix:

    def __init__(self):
        # intialize matrix according to dimensions
        matrix_segment = [0]*GRID[1]
        self.matrix = []
        for i in range(GRID[0]):
            self.matrix.append(deepcopy(matrix_segment))
        self.x_len, self.y_len = len(self.matrix[0]), len(self.matrix)
        self.addTwoNumbersAtStart()
        self.initializeFieldCenters()
    
    def initializeFieldCenters(self):
        self.fieldCenters = deepcopy(self.matrix)
        for y in range(self.y_len):
            for x in range(self.x_len):
                field_center = (BOX_HEIGHT/2 + BOX_HEIGHT*x, BOX_HEIGHT/2 + BOX_HEIGHT*y)
                self.fieldCenters[y][x] = field_center
        # print(matrixLineBreakString(self.fieldCenters))

    def __str__(self):
        return matrixLineBreakString(self.matrix)

    def addTwoNumbersAtStart(self): # adds two numbers initially
        for i in range(2):
            rand_x = randint(0,self.x_len-1)
            rand_y = randint(0,self.y_len-1)
            element = self.matrix[rand_y][rand_x]
            if element==0:
                # generate 2 with higher chance
                self.matrix[rand_y][rand_x] = (randint(1,3) % 2 + 1) * 2
            else:
                self.__init__()

    def up(self):
        self.matrix = pullUp(self.matrix)
        # print('done')
        # print(matrixLineBreakString(self.matrix))

    def down(self):
        rotatedMatrix = rotateMatrixClock(rotateMatrixClock(self.matrix))
        pushedMatrix = pullUp(rotatedMatrix)
        self.matrix = rotateMatrixAnticlock(rotateMatrixAnticlock(pushedMatrix))

    def left(self):
        rotatedMatrix = rotateMatrixClock(self.matrix)
        pushedMatrix = pullUp(rotatedMatrix)
        self.matrix = rotateMatrixAnticlock(pushedMatrix)

    def right(self):
        rotatedMatrix = rotateMatrixAnticlock(self.matrix)
        pushedMatrix = pullUp(rotatedMatrix)
        self.matrix = rotateMatrixClock(pushedMatrix)

game_matrix = GameMatrix()

def main():
    pygame.init()
    pygame.font.init()
    # clock = pygame.time.Clock()
    myfont = pygame.font.SysFont(name='',size=60)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    running = True
    RenderNewMatrix = True

    while running:
        # Did the user click the window close button?
        event_list = pygame.event.get()
        for tempEvent in event_list:
            if tempEvent.type == pygame.QUIT:
                running = False
            elif tempEvent.type == KEYDOWN:
                if tempEvent.key == K_UP:
                    print('up')
                    game_matrix.up()
                elif tempEvent.key == K_DOWN:
                    print('down')
                    game_matrix.down()
                elif tempEvent.key == K_LEFT:
                    print('left')
                    game_matrix.left()
                elif tempEvent.key == K_RIGHT:
                    print('right')
                    game_matrix.right()
                else:
                    pass
                RenderNewMatrix = True
            # print(event_list)

        # Fill the background with beige
        screen.fill((189,175,159))

        for dimension in range(2):
            for lineindex in range(1,GRID[dimension]):
                segment_index = SCREEN_DIMENSIONS[dimension]/(GRID[dimension])*lineindex
                if dimension == 1:
                    pygame.draw.line(screen, (0,0,0), (segment_index,0), (segment_index,SCREEN_HEIGHT), width=2)
                else:
                    pygame.draw.line(screen, (0,0,0), (0,segment_index), (SCREEN_WIDTH,segment_index), width=2)

        if RenderNewMatrix is True:
            listOfNonZero = []
            for y in range(game_matrix.y_len):
                for x in range(game_matrix.x_len):
                    if game_matrix.matrix[y][x] != 0:
                        listOfNonZero.append((x,y))
            RenderNewMatrix = False
        for x,y in listOfNonZero:
            font = myfont.render(str(game_matrix.matrix[y][x]), True, (0, 0, 0))
            textRect = font.get_rect(center=(game_matrix.fieldCenters[y][x][0], game_matrix.fieldCenters[y][x][1]))
            screen.blit(font, textRect)
        pygame.display.flip()
    pygame.quit()

def trial():
    print('init:')
    print(game_matrix)
    game_matrix.up()
    print('result:')
    print(game_matrix)

if __name__ == "__main__":
    main()