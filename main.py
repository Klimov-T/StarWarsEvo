from math import cos, sin
import random
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
        self.exist = True
        self.newObjects = []
        self.prevPosition = Vector()
        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()
        self.anglePos = 0
        self.angleVel = 0
        self.angleAcc = 0
        self.collisionR = 0
    def setPos(self, pos = Vector(), angle = 0):
        self.prevPosition = pos
        self.position = pos
        self.anglePos = angle
    def setVel(self, vel = Vector(), angle = 0):
        self.velocity = vel
        self.angleVel = angle
    def setAcc(self, acc = Vector(), angle = 0):
        self.acceleration = acc
        self.angleAcc = angle
    def setR(self, R = 0):
        self.collisionR = R
    def dPos(self, dPosition = Vector(), dA = 0):
        self.prevPosition += dPosition
        self.position += dPosition
        self.anglePos += dA
    def dT(self, dt, keys):
        self.velocity += self.acceleration * dt
        self.prevPosition = self.position
        self.position += self.velocity * dt
        self.angleVel += self.angleAcc * dt
        self.anglePos += self.angleVel * dt
    def collision(self, other):
        a = 1.0 * ((self.position.Xpos - self.prevPosition.Xpos) - (other.position.Xpos - other.prevPosition.Xpos))
        b = 1.0 * (self.prevPosition.Xpos - other.prevPosition.Xpos)
        c = 1.0 * ((self.position.Ypos - self.prevPosition.Ypos) - (other.position.Ypos - other.prevPosition.Ypos))
        d = 1.0 * (self.prevPosition.Ypos - other.prevPosition.Ypos)
        e = a**2 + c**2
        if e == 0:
            if (abs(other.position - self.position) < (self.collisionR + other.collisionR)):
                return True
            else:
                return False
        else:
            t = -(a*b+c*d) / e
            if t < 0:
                if (abs(other.prevPosition - self.prevPosition) < (self.collisionR + other.collisionR)):
                    return True
                else:
                    return False
            if t > 1:
                if (abs(other.position - self.position) < (self.collisionR + other.collisionR)):
                    return True
                else:
                    return False
            if t >= 0 and t <= 1:
                pos1 = self.prevPosition + (self.position-self.prevPosition) * t
                pos2 = other.prevPosition + (other.position-other.prevPosition) * t
                if (abs(pos1 - pos2) < (self.collisionR + other.collisionR)):
                    return True
                else:
                    return False
    def collisionAction(self, other):
        pass
    def __str__(self):
        return('pos = (' + str(self.position) + '); ' + 'vel = (' + str(self.velocity) + '); ' + 'acc = (' + str(self.acceleration) + '); ' + 'aPos = (' + str(self.anglePos) + '); ' + 'aVel = (' + str(self.angleVel) + '); ' + 'aAcc = (' + str(self.angleAcc) + ');')
    def draw(self, window, FPVObj, scale = 1):
        pass
    def getNewObjects(self):
        return self.newObjects
    def clearNewObjects(self):
        self.newObjects = []

SCREENX = 1920
SCREENY = 1080
screenScale = 1.0
FPVObject = 0

class Ball(PhysObject):
    def __init__(self):
        super().__init__()
        self.color = pygame.Color(255, 255, 255, 255)
    def draw(self, window, FPVObj = PhysObject(), scale = 1):
        pygame.draw.circle(window, self.color, (SCREENX/2 + (self.position.Xpos-FPVObj.position.Xpos) * scale, SCREENY/2 + (self.position.Ypos-FPVObj.position.Ypos) * scale), self.collisionR * scale, width = 0)
    def collisionAction(self, other):
        self.exist = False

class ActiveBall(Ball):
    def __init__(self):
        super().__init__()
    def dT(self, dt, keys):
        ax = ay = 0
        if (keys[pygame.K_w]): ay -= 1000
        if (keys[pygame.K_a]): ax -= 1000
        if (keys[pygame.K_s]): ay += 1000
        if (keys[pygame.K_d]): ax += 1000
        self.acceleration.setXY(ax, ay)
        super().dT(dt, keys)
    def collisionAction(self, other):
        self.collisionR += 5

class Bullet(PhysObject):
    def __init__(self, pos = Vector(0, 0), vel = Vector(0, 0), owner = any):
        super().__init__()
        self.lifetime = 5.0
        self.visionR = 10
        self.collisionR = 5
        self.position = pos
        self.velocity = vel
        self.damage = 1
        self.owner = owner
        self.color = pygame.Color(random.randint(150, 255), random.randint(150, 255), random.randint(150, 255), 255)
    def collisionAction(self, other):
        if other != self.owner:
            if type(other) == Bullet:
                if other.owner != self.owner:
                    self.exist = False
            else:
                self.exist = False
    def draw(self, window, FPVObj, scale=1):
        pygame.draw.circle(window, self.color, (SCREENX/2 + (self.position.Xpos-FPVObj.position.Xpos) * scale, SCREENY/2 + (self.position.Ypos-FPVObj.position.Ypos) * scale), self.visionR * scale, width = 0)
    def dT(self, dt, keys):
        super().dT(dt, keys)
        self.lifetime -= dt
        if self.lifetime <= 0: self.exist = False

class Gun(ActiveBall):
    def __init__(self):
        super().__init__()
    def dT(self, dt, keys):
        super().dT(dt, keys)
        if (keys[pygame.K_SPACE]): self.newObjects.append(Bullet(self.position, self.velocity+Vector(0, -1000), self))
    def collisionAction(self, other):
        pass

class Map(object):
    def __init__(self):
        self.objects = []
    def addObject(self, obj):
        self.objects.append(obj)
    def dT(self, dt, keys):
        for i in self.objects:
            i.dT(dt, keys)
    def draw(self, window, FPVObj = PhysObject(), scale = 1):
        for i in self.objects:
            i.draw(window, FPVObj, scale)
    def collision(self):
        l = len(self.objects)
        for i in range(l):
            for j in range(l-i-1):
                if self.objects[i].collision(self.objects[i+j+1]):
                    self.objects[i].collisionAction(self.objects[i+j+1])
                    self.objects[i+j+1].collisionAction(self.objects[i])
    def cleanObj(self):
        newObjects = []
        for i in self.objects:
            if i.exist: newObjects.append(i)
        self.objects = newObjects
    def addNewObjects(self):
        for i in self.objects:
            for j in i.getNewObjects():
                self.objects.append(j)
            i.clearNewObjects()
    

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((SCREENX, SCREENY))
    clock = pygame.time.Clock()
    gameMap = Map()

def init_window():
    pygame.display.set_caption('Star Wars')
 
def init_map():
    global FPVObject
    obj = Gun()
    obj.setPos(Vector(0, 0))
    obj.setR(20)
    FPVObject = obj
    gameMap.addObject(obj)
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
    global screenScale, FPVObject
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        dt = pygame.time.get_ticks() - clk
        clk = pygame.time.get_ticks()
        window.fill((0, 0, 0, 0))
        if (keys[pygame.K_MINUS]): screenScale *= 0.9999**(1.0*dt*10)
        if (keys[pygame.K_EQUALS]): screenScale *= 1.0001**(1.0*dt*10)
        gameMap.dT(1.0*dt*0.001, keys)
        gameMap.collision()
        gameMap.addNewObjects()
        gameMap.cleanObj()
        gameMap.draw(window, FPVObject, screenScale)
        pygame.display.flip()
 
if __name__ == '__main__': main()