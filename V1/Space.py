import pygame
import time
pygame.font.init()
SquareFont = pygame.font.SysFont('arial ', 50)

class Space:
    def __init__(self,x,y,jewel,surface,squareSize):
        self.x = x
        self.y = y
        self.jewel = jewel
        self.surface = surface
        self.squareSize = squareSize
        self.isSelected = False
        self.points = self.jewel * 100
        self.color = (0,0,0)

        self.getColor()
        
    def getColor(self):
        if self.jewel == 0:
            self.color = (0,0,0)
        if self.jewel == 1:
            self.color = (220,20,60)
        if self.jewel == 2:
            self.color = (50,205,50)
        if self.jewel == 3:
            self.color = (0,191,255)
        if self.jewel == 4:
            self.color = (255,215,0)
        if self.jewel == 5:
            self.color = (138,43,226)

    def draw(self):
        if self.jewel != 0:
            if self.isSelected:
                pygame.draw.circle(self.surface, (200,200,200),(self.x * self.squareSize + self.squareSize/2,self.y * self.squareSize + self.squareSize/2),self.squareSize/2.5)
            else:
                pygame.draw.circle(self.surface, (0,0,0),(self.x * self.squareSize + self.squareSize/2,self.y * self.squareSize + self.squareSize/2),self.squareSize/2.5)
            pygame.draw.circle(self.surface, self.color,(self.x * self.squareSize + self.squareSize/2,self.y * self.squareSize + self.squareSize/2),self.squareSize/3)
        hSurf = SquareFont.render(str(self.jewel), True, (255,255,255))
        #self.surface.blit(hSurf,(self.x * self.squareSize + self.squareSize/2.5 , self.y * self.squareSize + self.squareSize/3))

    def setJewel(self,jewel):
        self.jewel = jewel
        self.getColor()

    def __str__(self):
        return "X:" + str(self.x) + ", Y:" + str(self.y) + ", Jewel:" + str(self.jewel)
