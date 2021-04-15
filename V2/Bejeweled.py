import pygame
from Space import Space
import random
import math
import time
import os

WIDTH = 1400
HEIGHT = WIDTH-600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Bejeweled")
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
rows,cols = 7,7
squareSize = math.floor(HEIGHT/cols)
Selected = None
AnimationSpeed = 0.005
pygame.font.init()
pygame.mixer.init()
ScoreFont = pygame.font.SysFont('arial', math.floor(squareSize/2))
LegendFont = pygame.font.SysFont('arial', math.floor(squareSize/4))


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    
#Images Loading
current_dir = os.path.dirname(os.path.abspath(__file__))
bgPath = os.path.join(current_dir, "BejeweledBackground.png")
bgImage = pygame.image.load(bgPath)
GameMenuPath = os.path.join(current_dir, "GameMenuBackground.png")
GameMenuImage = pygame.image.load(GameMenuPath)

#Sound loading
SwapSoundPath = os.path.join(current_dir, "SwapSound.wav")
SwapSound = pygame.mixer.Sound(SwapSoundPath)
SwapBackSoundPath = os.path.join(current_dir, "SwapBackSound.wav")
SwapBackSound = pygame.mixer.Sound(SwapBackSoundPath)
SelectionSoundPath = os.path.join(current_dir, "SelectionSound.wav")
SelectionSound = pygame.mixer.Sound(SelectionSoundPath)
DeSelectionSoundPath = os.path.join(current_dir, "DeSelectionSound.wav")
DeSelectionSound = pygame.mixer.Sound(DeSelectionSoundPath)
DropDownSoundPath = os.path.join(current_dir, "DropDownSound.wav")
DropDownSound = pygame.mixer.Sound(DropDownSoundPath)
Match3Path = os.path.join(current_dir, "Match3Sound.wav")
Match3Sound = pygame.mixer.Sound(Match3Path)
Match4Path = os.path.join(current_dir, "Match4Sound.wav")
Match4Sound = pygame.mixer.Sound(Match4Path)
Match5Path = os.path.join(current_dir, "Match5Sound.wav")
Match5Sound = pygame.mixer.Sound(Match5Path)
GameMusicPath = os.path.join(current_dir, "GameMusic.wav")
GameMusic = pygame.mixer.music.load(GameMusicPath)
pygame.mixer.music.play(-1)


RedImage = Space.getImage(1)
GreenImage = Space.getImage(2)
BlueImage = Space.getImage(3)
YellowImage = Space.getImage(4)
PurpleImage = Space.getImage(5)

RedJewelText = LegendFont.render(" - 100 Points", True, (255,255,255))
GreenJewelText = LegendFont.render(" - 200 Points", True, (255,255,255))
BlueJewelText = LegendFont.render(" - 300 Points", True, (255,255,255))
YellowJewelText = LegendFont.render(" - 400 Points", True, (255,255,255))
PurpleJewelText = LegendFont.render(" - 500 Points", True, (255,255,255))
RedLegendImage = pygame.transform.scale(RedImage,(math.floor(squareSize/3),math.floor(squareSize/3)))
GreenLegendImage = pygame.transform.scale(GreenImage,(math.floor(squareSize/3),math.floor(squareSize/3)))
BlueLegendImage = pygame.transform.scale(BlueImage,(math.floor(squareSize/3),math.floor(squareSize/3)))
YellowLegendImage = pygame.transform.scale(YellowImage,(math.floor(squareSize/3),math.floor(squareSize/3)))
PurpleLegendImage = pygame.transform.scale(PurpleImage,(math.floor(squareSize/3),math.floor(squareSize/3)))


PlayerScore = 0
ComboMultiplier = []
BoardEnd = 0


def create2DArray():
    squares = []
    for x in range(rows):
        row = []
        for y in range(cols):
            col = random.randint(1,5)
            square = Space(x,y,col,WINDOW,squareSize)
            row.append(square)
        squares.append(row)
    return squares

squares = create2DArray()

def main():
    global GameMenuImage,bgImage,BoardEnd,PlayerScore
    clock = pygame.time.Clock()
    run = True
    BoardEnd = squares[6][6].y * squares[6][6].squareSize + squares[6][6].squareSize
    GameMenuImage = pygame.transform.scale(GameMenuImage,(WIDTH - BoardEnd,HEIGHT))
    bgImage = pygame.transform.scale(bgImage,(WIDTH - (WIDTH-BoardEnd),HEIGHT))
    checks = CheckMatches()
    while checks != []:
        RemoveMatches(checks)
        dropDownJewels(False)
        fillEmptySpaces(False)
        checks = CheckMatches()
    PlayerScore = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                checkMouseClick(event)
        doGameProcess(CheckMatches(),True)
        draw_all()
    pygame.quit()

def draw_all():
    global GameMenuImage,BoardEnd
    update_display()
    draw_BackGround()
    draw_Score()
    drawJewelLegend()
    #draw_window()
    draw_board()
    
def draw_board():
    for x in range(rows):
        for y in range(cols):
            squares[x][y].draw()

def draw_BackGround():
    WINDOW.blit(bgImage,(0,0),(0,0,BoardEnd,HEIGHT))
    WINDOW.blit(GameMenuImage,(BoardEnd,0))

def draw_Score():
    SSurf = ScoreFont.render(str(PlayerScore), True, (255,255,255))
    ScoreRect = SSurf.get_rect(center=(WIDTH-(WIDTH-BoardEnd)/2,squareSize/1.5))
    WINDOW.blit(SSurf, ScoreRect)

def drawJewelLegend():
    WINDOW.blit(RedJewelText,(WIDTH-(WIDTH-BoardEnd*1.15), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*4)))
    WINDOW.blit(GreenJewelText, (WIDTH-(WIDTH-BoardEnd*1.15), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*3)))
    WINDOW.blit(BlueJewelText, (WIDTH-(WIDTH-BoardEnd*1.15), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*2)))
    WINDOW.blit(YellowJewelText, (WIDTH-(WIDTH-BoardEnd*1.15), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*1)))
    WINDOW.blit(PurpleJewelText, (WIDTH-(WIDTH-BoardEnd*1.15), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*0)))
    WINDOW.blit(RedLegendImage,(WIDTH-(WIDTH-BoardEnd*1.1), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*4)))
    WINDOW.blit(GreenLegendImage,(WIDTH-(WIDTH-BoardEnd *1.1), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*3)))
    WINDOW.blit(BlueLegendImage,(WIDTH-(WIDTH-BoardEnd *1.1), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*2)))
    WINDOW.blit(YellowLegendImage,(WIDTH-(WIDTH-BoardEnd *1.1), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*1)))
    WINDOW.blit(PurpleLegendImage,(WIDTH-(WIDTH-BoardEnd *1.1), HEIGHT- (HEIGHT/8) - ((HEIGHT/8)/2*0)))

def SelectedAnim(Space):
        size = 0
        while size < Space.squareSize/2:
            draw_all()
            pygame.draw.circle(Space.surface, (255,255,255),(Space.x * Space.squareSize + Space.squareSize/2,Space.y * Space.squareSize + Space.squareSize/2),size)
            size += squareSize/7.6

def DeSelectedAnim(Space):
        size = Space.squareSize/2
        while size > 0:
            draw_all()
            pygame.draw.circle(Space.surface, (255,255,255),(Space.x * Space.squareSize + Space.squareSize/2,Space.y * Space.squareSize + Space.squareSize/2),size)
            size -= squareSize/7.6
    
def checkMouseClick(event):
    global Selected
    mouse = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    xIndex = math.floor((mouse_pos[0]/squareSize))
    yIndex = math.floor((mouse_pos[1]/squareSize))
    if mouse_pos[0] >= squares[6][6].y * squares[6][6].squareSize + squares[6][6].squareSize:
        print("On Menu")
    else:
        if event.button == 1: #left click
            if Selected != None:
                if Selected == squares[xIndex][yIndex]:
                    squares[xIndex][yIndex].isSelected = False
                    DeSelectionSound.play()
                    DeSelectedAnim(squares[xIndex][yIndex])
                    Selected = None
                else:
                    if squares[xIndex][yIndex].jewel != 0:
                        Selected.isSelected = False
                        DeSelectedAnim(Selected)
                        SelectionSound.play()
                        SelectedAnim(squares[xIndex][yIndex])
                        squares[xIndex][yIndex].isSelected = True
                        Selected = squares[xIndex][yIndex]
            else:
                if squares[xIndex][yIndex].jewel != 0:
                    Selected = squares[xIndex][yIndex]
                    SelectionSound.play()
                    SelectedAnim(squares[xIndex][yIndex])
                    squares[xIndex][yIndex].isSelected = True
        if event.button == 2:
            ShuffleBoard()
        if event.button == 3:
            if Selected != None and Selected != squares[xIndex][yIndex] and squares[xIndex][yIndex] in checkNeighbours(Selected.x,Selected.y) and squares[xIndex][yIndex].jewel != 0:
                Selected.isSelected = False
                swapSpaces(Selected,squares[xIndex][yIndex],False)
                Selected = None

def ShuffleBoard():
    for x in squares:
        for y in x:
            y.setJewel(0)
    fillEmptySpaces(False)
    checks = CheckMatches()
    while checks != []:
        RemoveMatches(checks)
        dropDownJewels(False)
        fillEmptySpaces(False)
        checks = CheckMatches()

def swapSpaces(Space1,Space2, isSwapback):
    global squares
    SwapBackSound.stop()
    SwapSound.stop()
    SP1J = Space1.jewel
    SP2J = Space2.jewel
    SP1C = Space1.image
    SP2C = Space2.image

    Space1.setJewel(0)
    Space2.setJewel(0)
    if isSwapback:
        SwapBackSound.play()
    else:
        SwapSound.play()
    swapAnim(Space1,Space2,SP1C,SP2C)
    Space1.setJewel(SP2J)
    Space2.setJewel(SP1J)

    checks = CheckMatches()
    if checks == [] and not isSwapback:
        swapSpaces(Space2,Space1,True)
    else:
        doGameProcess(checks,True)
        
def doGameProcess(checks,doAnims):
    RemoveMatches(checks)
    AddScore(checks)
    dropDownJewels(doAnims)
    fillEmptySpaces(doAnims)

def AddScore(checks):
    global PlayerScore,ComboMultiplier
    if checks != []:
        for i in checks:
            AddScore = (i[0].points * len(i)) * len(checks)
            #print("Single Match Score:" + str(AddScore))
            ComboMultiplier.append(AddScore)
    else:
        Score = 0
        for x in ComboMultiplier:
            Score += x
        #if len(ComboMultiplier) != 0:
            #print("Final Score:" + str(Score))
            #print(len(ComboMultiplier))
            #print(Score * len(ComboMultiplier))
        PlayerScore += (Score * len(ComboMultiplier))
        ComboMultiplier = []

        #Animation for counting up score
        #Add +Score next to matches
    
def dropDownJewels(doAnims):
    global squares
    for i in range(len(squares)):
        j= len(squares[i])-1
        while(j > 0):
            if squares[i][j].jewel == 0 and squares[i][j-1].jewel != 0:
                image = squares[i][j-1].image
                jewel = squares[i][j-1].jewel
                squares[i][j-1].setJewel(0)
                if doAnims:
                    #print("Hello" + str(j))
                    #DropDownSound.play()
                    dropDownJewelsAnim(squares[i][j-1],squares[i][j],image)
                squares[i][j].setJewel(jewel)
                j = len(squares[i])
            j -= 1

def fillEmptySpaces(doAnims):
    for i in range(cols):
        for j in range(rows-1,-1,-1):
            if squares[i][j].jewel == 0:
                col = random.randint(1,5)
                if doAnims:
                    DropDownSound.play()
                    fillEmptySpacesAnim(squares[i][j],Space.getImage(col))
                squares[i][j].setJewel(col)

def RemoveMatches(checks):
    for i in checks:
        for j in i:
            squares[j.x][j.y].setJewel(0)

def swapAnim(Space1,Space2,img1,img2):
    #AnimAmount = squareSize/7.6
    AnimAmount = squareSize/10

    img1 = pygame.transform.scale(img1,(math.floor(Space1.squareSize/1.5),math.floor(Space1.squareSize/1.5)))
    img2 = pygame.transform.scale(img2,(math.floor(Space2.squareSize/1.5),math.floor(Space2.squareSize/1.5)))
    loopX = Space1.x * Space1.squareSize + Space1.squareSize/6
    loopY = Space1.y * Space1.squareSize + Space1.squareSize/6
    YoopX = Space2.x * Space2.squareSize + Space2.squareSize/6
    YoopY = Space2.y * Space2.squareSize + Space2.squareSize/6

    SP2X = YoopX
    SP2Y = YoopY


    if Space2.x < Space1.x:
        while SP2X < loopX:
            WINDOW.blit(img2,(YoopX,YoopY))
            WINDOW.blit(img1,(loopX,loopY))
            
            loopX -= AnimAmount
            YoopX += AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.x > Space1.x:
        while SP2X > loopX:
            WINDOW.blit(img2,(YoopX,YoopY))
            WINDOW.blit(img1,(loopX,loopY))

            loopX += AnimAmount
            YoopX -= AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.y < Space1.y:
        while SP2Y < loopY:
            WINDOW.blit(img2,(YoopX,YoopY))
            WINDOW.blit(img1,(loopX,loopY))

            loopY -= AnimAmount
            YoopY += AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()
    if Space2.y > Space1.y:
        while SP2Y > loopY:
            WINDOW.blit(img2,(YoopX,YoopY))
            WINDOW.blit(img1,(loopX,loopY))

            loopY += AnimAmount
            YoopY -= AnimAmount
            time.sleep(AnimationSpeed)
            draw_all()

def dropDownJewelsAnim(Space1,Space2,img1):
    AnimAmount = 40
    img1 = pygame.transform.scale(img1,(math.floor(Space1.squareSize/1.5),math.floor(Space1.squareSize/1.5)))

    loopX = Space1.x * Space1.squareSize + Space1.squareSize/6
    loopY = Space1.y * Space1.squareSize + Space1.squareSize/6
    YoopX = Space2.x * Space2.squareSize + Space2.squareSize/6
    YoopY = Space2.y * Space2.squareSize + Space2.squareSize/6

    SP2X = YoopX
    SP2Y = YoopY
    while SP2Y > loopY:
        WINDOW.blit(img1,(loopX,loopY))
        loopY += AnimAmount
        time.sleep(AnimationSpeed)
        draw_all()

def fillEmptySpacesAnim(Space,img1):
    AnimAmount = 40
    img1 = pygame.transform.scale(img1,(math.floor(Space.squareSize/1.5),math.floor(Space.squareSize/1.5)))

    loopX = Space.x * Space.squareSize + Space.squareSize/6
    loopY = 0 - Space.squareSize/3
    YoopY = Space.y * Space.squareSize + Space.squareSize/6

    while YoopY > loopY:
        WINDOW.blit(img1,(loopX,loopY))
        loopY += AnimAmount
        time.sleep(AnimationSpeed)
        draw_all()

def RemoveMatchesAnim(Spaces):
    pass

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
            if len(groups) == 3:
                Match3Sound.play()
            if len(groups) == 4:
                Match4Sound.play()
            if len(groups) == 5:
                Match5Sound.play()
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
            if len(groups) == 3:
                Match3Sound.play()
            if len(groups) == 4:
                Match4Sound.play()
            if len(groups) == 5:
                Match5Sound.play()
            matches.append(groups)
    return matches

def draw_window():
    WINDOW.fill(BLACK)

def update_display():
    pygame.display.flip()

def getImage(col):
        if col == 0:
            return BlueImage
        if col == 1:
            return RedImage
        if col == 2:
            return GreenImage
        if col == 3:
            return BlueImage
        if col == 4:
            return YellowImage
        if col == 5:
            return PurpleImage

if __name__ == "__main__":
    main()
