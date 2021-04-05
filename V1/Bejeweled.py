import pygame
from Space import Space
import random
import math
import time

WIDTH,HEIGHT = 1000,1000 
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bejeweled")
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
rows,cols = 7,7
squareSize = max(WIDTH,HEIGHT)/max(rows,cols)
Selected = None
AnimationSpeed = 0.005

def create2DArray():
    squares = []
    for x in range(rows):
        row = []
        for y in range(cols):
            square = Space(x,y,random.randint(1,5),WINDOW,squareSize)
            row.append(square)
        squares.append(row)
    return squares

squares = create2DArray()

def main():
    
    #fillEmptySpaces()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClick(event)
        RemoveMatches(CheckMatches())
        dropDownJewels()
        fillEmptySpaces()
        draw_all()
    pygame.quit()

def draw_all():
    update_display()
    draw_window()
    draw_board()

def draw_board():
    for x in range(rows):
        for y in range(cols):
            squares[x][y].draw()
            
def checkMouseClick(event):
    global Selected
    mouse = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    xIndex = math.floor((mouse_pos[0]/squareSize))
    yIndex = math.floor((mouse_pos[1]/squareSize))
    if event.button == 1: #left click
        if Selected != None:
            if Selected == squares[xIndex][yIndex]:
                squares[xIndex][yIndex].isSelected = False
                Selected = None
            else:
                if squares[xIndex][yIndex].jewel != 0:
                    Selected.isSelected = False
                    squares[xIndex][yIndex].isSelected = True
                    Selected = squares[xIndex][yIndex]
        else:
            if squares[xIndex][yIndex].jewel != 0:
                Selected = squares[xIndex][yIndex]
                squares[xIndex][yIndex].isSelected = True
    if event.button == 2:
        dropDownJewels()
    if event.button == 3:
        if Selected != None and Selected != squares[xIndex][yIndex] and squares[xIndex][yIndex] in checkNeighbours(Selected.x,Selected.y) and squares[xIndex][yIndex].jewel != 0:
            Selected.isSelected = False
            swapSpaces(Selected,squares[xIndex][yIndex],False)
            Selected = None

def swapSpaces(Space1,Space2, isSwapback):
    global squares
    SP1J = Space1.jewel
    SP2J = Space2.jewel
    SP1C = Space1.color
    SP2C = Space2.color

    Space1.setJewel(0)
    Space2.setJewel(0)

    swapAnim(Space1,Space2,SP1C,SP2C)
    #pygame.draw.circle(Space1.surface, Space1.color,(Space1.x * Space1.squareSize + Space1.squareSize/2,Space1.y * Space1.squareSize + Space1.squareSize/2),Space1.squareSize/3)
    Space1.setJewel(SP2J)
    #pygame.draw.circle(Space2.surface, Space2.color,(Space2.x * Space2.squareSize + Space2.squareSize/2,Space2.y * Space2.squareSize + Space2.squareSize/2),Space2.squareSize/3)
    Space2.setJewel(SP1J)

    checks = CheckMatches()
    if checks == [] and not isSwapback:
        swapSpaces(Space2,Space1,True)
    else:
        RemoveMatches(checks)
        dropDownJewels()
        fillEmptySpaces()

def dropDownJewels():
    global squares
    for i in range(len(squares)):
        j= len(squares[i])-1
        while(j > 0):
            if squares[i][j].jewel == 0 and squares[i][j-1].jewel != 0:
                col = squares[i][j-1].color
                jewel = squares[i][j-1].jewel
                squares[i][j-1].setJewel(0)
                dropDownJewelsAnim(squares[i][j-1],squares[i][j],col)
                squares[i][j].setJewel(jewel)
                j = len(squares[i])
            j -= 1

def fillEmptySpaces():
    for i in range(cols):
        for j in range(rows-1,-1,-1):
            if squares[i][j].jewel == 0:
                col = random.randint(1,5)
                fillEmptySpacesAnim(squares[i][j],getColor(col))
                squares[i][j].setJewel(col)

def RemoveMatches(checks):
    for i in checks:
        for j in i:
            squares[j.x][j.y].setJewel(0)

def swapAnim(Space1,Space2,col1,col2):
    AnimAmount = 3
    loopX = Space1.x * Space1.squareSize + Space1.squareSize/2
    loopY = Space1.y * Space1.squareSize + Space1.squareSize/2
    YoopX = Space2.x * Space2.squareSize + Space2.squareSize/2
    YoopY = Space2.y * Space2.squareSize + Space2.squareSize/2

    SP2X = YoopX
    SP2Y = YoopY


    if Space2.x < Space1.x:
        while SP2X < loopX:
            pygame.draw.circle(Space1.surface, col1,(loopX,loopY),Space1.squareSize/3)
            pygame.draw.circle(Space2.surface, col2,(YoopX,YoopY),Space2.squareSize/3)
            loopX -= AnimAmount
            YoopX += AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.x > Space1.x:
        while SP2X > loopX:
            pygame.draw.circle(Space1.surface, col1,(loopX,loopY),Space1.squareSize/3)
            pygame.draw.circle(Space2.surface, col2,(YoopX,YoopY),Space2.squareSize/3)
            loopX += AnimAmount
            YoopX -= AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.y < Space1.y:
        while SP2Y < loopY:
            pygame.draw.circle(Space1.surface, col1,(loopX,loopY),Space1.squareSize/3)
            pygame.draw.circle(Space2.surface, col2,(YoopX,YoopY),Space2.squareSize/3)
            loopY -= AnimAmount
            YoopY += AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.y > Space1.y:
        while SP2Y > loopY:
            pygame.draw.circle(Space1.surface, col1,(loopX,loopY),Space1.squareSize/3)
            pygame.draw.circle(Space2.surface, col2,(YoopX,YoopY),Space2.squareSize/3)
            loopY += AnimAmount
            YoopY -= AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()

def dropDownJewelsAnim(Space1,Space2,col1):
    AnimAmount = 10
    loopX = Space1.x * Space1.squareSize + Space1.squareSize/2
    loopY = Space1.y * Space1.squareSize + Space1.squareSize/2
    YoopX = Space2.x * Space2.squareSize + Space2.squareSize/2
    YoopY = Space2.y * Space2.squareSize + Space2.squareSize/2

    SP2X = YoopX
    SP2Y = YoopY

    while SP2Y > loopY:
        pygame.draw.circle(Space1.surface, col1,(loopX,loopY),Space1.squareSize/3)
        loopY += AnimAmount
        time.sleep(AnimationSpeed)
        draw_all()

def fillEmptySpacesAnim(Space,col):
    AnimAmount = 10
    loopX = Space.x * Space.squareSize + Space.squareSize/2
    loopY = 0 - Space.squareSize/3
    YoopY = Space.y * Space.squareSize + Space.squareSize/2
    print(col)

    while YoopY > loopY:
        pygame.draw.circle(Space.surface, col,(loopX,loopY),Space.squareSize/3)
        pygame.draw.circle(Space.surface, col,(loopX,loopY),Space.squareSize/3)
        loopY += AnimAmount
        time.sleep(AnimationSpeed)
        draw_all()

def checkNeighbours(x,y):
    neighbours = []
    if x < cols -1:
        neighbours.append(squares[x+1][y])
    if x > 0:
        neighbours.append(squares[x-1][y])
    if y < rows -1:
        neighbours.append(squares[x][y+1])
    if y > 0:
        neighbours.append(squares[x][y-1])
    return neighbours

def CheckMatches():
    global squares
    matches = []
    groups = []

    #Check for horizontal matches
    for i in range(len(squares)):
        tempArr = squares[i]
        groups = []
        for j in range(len(tempArr)):
            if j < len(tempArr) - 2:
                if squares[i][j] and squares[i][j + 1] and squares[i][j + 2]:
                    if squares[i][j].jewel == squares[i][j+1].jewel and squares[i][j+1].jewel == squares[i][j+2].jewel and squares[i][j].jewel != 0:
                        if len(groups) > 0:
                            if squares[i][j] not in groups:
                                matches.append(groups)
                                groups = []
                        if squares[i][j] not in groups:
                            groups.append(squares[i][j])
                        if squares[i][j+1] not in groups:
                            groups.append(squares[i][j+1])
                        if squares[i][j+2] not in groups:
                            groups.append(squares[i][j+2])
        if len(groups) > 0:
            matches.append(groups)

    # //Check for vertical matches
    for j in range(len(squares)):
        tempArr = squares[j]
        groups = []
        for i in range(len(tempArr)):
            if i < len(tempArr) - 2:
                if squares[i][j] and squares[i+1][j] and squares[i+2][j]:
                    if squares[i][j].jewel == squares[i+1][j].jewel and squares[i+1][j].jewel == squares[i+2][j].jewel and squares[i][j].jewel != 0:
                        if len(groups) > 0:
                            if squares[i][j] not in groups:
                                matches.append(groups)
                                groups = []
                        if squares[i][j] not in groups:
                            groups.append(squares[i][j])
                        if squares[i+1][j] not in groups:
                            groups.append(squares[i+1][j])
                        if squares[i+2][j] not in groups:
                            groups.append(squares[i+2][j])
        if len(groups) > 0:
            matches.append(groups)
    return matches

def draw_window():
    WINDOW.fill(BLACK)

def update_display():
    pygame.display.flip()

def getColor(col):
        if col == 0:
            return (0,0,0)
        if col == 1:
            return (220,20,60)
        if col == 2:
            return (50,205,50)
        if col == 3:
            return (0,191,255)
        if col == 4:
            return (255,215,0)
        if col == 5:
            return (138,43,226)

if __name__ == "__main__":
    main()
