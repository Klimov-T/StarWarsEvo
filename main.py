from math import cos, sin
import pygame
import sys






class Vector(object):
    def __init__(self, x = 0, y = 0):
        self.Xpos = x
        self.Ypos = y
    def setXY(self, x = 0, y = 0):
        self.Xpos = x
        self.Ypos = y
    def __add__(self, other):
        return Vector(self.Xpos + other.Xpos, self.Ypos + other.Ypos)
    def __sub__(self, other):
        return Vector(self.Xpos - other.Xpos, self.Ypos - other.Ypos)
    def __mul__(self, other):
        return Vector(self.Xpos * other, self.Ypos * other)
    def __pow__(self, other):
        return (self.Xpos*other.Xpos + self.Ypos*other.Ypos)
    def __truediv__(self, other):
        return Vector(self.Xpos / other, self.Ypos / other)
    def __abs__(self):
        return ((self.Xpos**2 + self.Ypos**2)**0.5)
    def __str__(self):
        return('x = ' + str(self.Xpos) + '; y = ' + str(self.Ypos) + ';')
    def rot(self, angle):
        ansX = cos(angle) * self.Xpos - sin(angle) * self.Ypos
        ansY = sin(angle) * self.Xpos + cos(angle) * self.Ypos
        self.Xpos = ansX
        self.Ypos = ansY

class PhysObject(object):
    def __init__(self):
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        self.anglePos = 0
        self.angleVel = 0
        self.angleAcc = 0
        self.colisionR = 0
    def setPos(self, pos = Vector(), angle = 0):
        self.position = pos
        self.anglePos = angle
    def setVel(self, vel = Vector(), angle = 0):
        self.velocity = vel
        self.angleVel = angle
    def setAcc(self, acc = Vector(), angle = 0):
        self.acceleration = acc
        self.angleAcc = angle
    def setR(self, R = 0):
        self.colisionR = R
    def dPos(self, dPosition = Vector(), dA = 0):
        self.position += dPosition
        self.anglePos += dA
    def dT(self, dt = 0):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.angleVel += self.angleAcc * dt
        self.anglePos += self.angleVel * dt
    def collision(self, other):
        if (abs(other.position - self.position) < (self.colisionR + other.colisionR)):
            return True
        else:
            return False
    def __str__(self):
        return('pos = (' + str(self.position) + '); ' + 'vel = (' + str(self.velocity) + '); ' + 'acc = (' + str(self.acceleration) + '); ' + 'aPos = (' + str(self.anglePos) + '); ' + 'aVel = (' + str(self.angleVel) + '); ' + 'aAcc = (' + str(self.angleAcc) + ');')

class Ball(PhysObject):
    def __init__(self):
        super().__init__()
        self.color = pygame.Color(255, 255, 255, 255)
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.position.Xpos, self.position.Ypos), self.colisionR, width = 0)

class Map(object):
    def __init__(self):
        self.objects = []
    def addObject(self, obj):
        self.objects.append(obj)
    def dT(self, dt):
        for i in self.objects:
            i.dT(dt)
    def draw(self, window):
        for i in self.objects:
            try:
                i.draw(window)
            except Warning as e:
                print(e)


pygame.init()
window = pygame.display.set_mode((1920, 1080))
gameMap = Map()

def init_window():
    pygame.display.set_caption('Star Wars')
 
def init_map():
    obj = Ball()
    obj.setPos(Vector(50, 50))
    obj.setAcc(Vector(1, 1))
    obj.setR(10)
    gameMap.addObject(obj)
    obj = Ball()
    obj.setPos(Vector(150, 150))
    obj.setAcc(Vector(0, 1))
    obj.setR(10)
    gameMap.addObject(obj)
    obj = Ball()
    obj.setPos(Vector(250, 250))
    obj.setAcc(Vector(1, 0))
    obj.setR(10)
    gameMap.addObject(obj)

def main():
    init_window()
    init_map()
    clk = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        dt = pygame.time.get_ticks() - clk
        clk = pygame.time.get_ticks()
        gameMap.dT(0.01)
        print(gameMap.objects[1])
        gameMap.draw(window)
        pygame.display.flip()
        pygame.time.delay(0)
 
if __name__ == '__main__': main()