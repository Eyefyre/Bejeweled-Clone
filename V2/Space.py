import pygame
import time
import math
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
GreenPath = os.path.join(current_dir, "GreenJewel.png")
GreenImage = pygame.image.load(GreenPath)
BluePath = os.path.join(current_dir, "BlueJewel.png")
BlueImage = pygame.image.load(BluePath)
YellowPath = os.path.join(current_dir, "YellowJewel.png")
YellowImage = pygame.image.load(YellowPath)
RedPath = os.path.join(current_dir, "RedJewel.png")
RedImage = pygame.image.load(RedPath)
PurplePath = os.path.join(current_dir, "PurpleJewel.png")
PurpleImage = pygame.image.load(PurplePath)

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
        self.image = BlueImage

        self.setJewel(jewel)

    @staticmethod
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

    def draw(self):
        if self.jewel != 0:
            if self.isSelected:
                pygame.draw.circle(self.surface, (255,255,255),(self.x * self.squareSize + self.squareSize/2,self.y * self.squareSize + self.squareSize/2),self.squareSize/2)
            img = pygame.transform.scale(self.image,(math.floor(self.squareSize/1.5),math.floor(self.squareSize/1.5)))
            self.surface.blit(img,(self.x * self.squareSize + self.squareSize/6,self.y * self.squareSize + self.squareSize/6))
        hSurf = SquareFont.render(str(self.jewel), True, (255,255,255))
        #self.surface.blit(hSurf,(self.x * self.squareSize + self.squareSize/2.5 , self.y * self.squareSize + self.squareSize/3))

    def setJewel(self,jewel):
        self.jewel = jewel
        self.image = self.getImage(self.jewel)

    def __str__(self):
        return "X:" + str(self.x) + ", Y:" + str(self.y) + ", Jewel:" + str(self.jewel)
