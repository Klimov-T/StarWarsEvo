from math import cos, sin
import random
import pygame
import sys





SCREENX = 1920
SCREENY = 1080
screenScale = 1.0
FPVObject = 0
gameMap = -1    # -1 means further initialisation
window = -1
clock = -1

class PhysObject(object):
    def __init__(self):
        self.exist = True
        self.newObjects = []
        self.prevPosition = pygame.Vector2()
        self.position = pygame.Vector2()
        self.velocity = pygame.Vector2()
        self.acceleration = pygame.Vector2()
        self.anglePos = 0
        self.angleVel = 0
        self.angleAcc = 0
        self.collisionR = 0
    def setPos(self, pos = pygame.Vector2(), angle = 0):
        self.prevPosition = pygame.Vector2(pos)
        self.position = pygame.Vector2(pos)
        self.anglePos = angle
    def setVel(self, vel = pygame.Vector2(), angle = 0):
        self.velocity = pygame.Vector2(vel)
        self.angleVel = angle
    def setAcc(self, acc = pygame.Vector2(), angle = 0):
        self.acceleration = pygame.Vector2(acc)
        self.angleAcc = angle
    def setR(self, R = 0):
        self.collisionR = R
    def dPos(self, dPosition = pygame.Vector2(), dA = 0):
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
        a = 1.0 * ((self.position.x - self.prevPosition.x) - (other.position.x - other.prevPosition.x))
        b = 1.0 * (self.prevPosition.x - other.prevPosition.x)
        c = 1.0 * ((self.position.y - self.prevPosition.y) - (other.position.y - other.prevPosition.y))
        d = 1.0 * (self.prevPosition.y - other.prevPosition.y)
        e = a**2 + c**2
        Rr = self.collisionR + other.collisionR
        if e == 0:
            if ((other.position - self.position).magnitude() < Rr):
                return True
            else:
                return False
        else:
            t = -(a*b+c*d) / e
            if t < 0:
                if ((other.prevPosition - self.prevPosition).magnitude() < Rr):
                    return True
                else:
                    return False
            if t > 1:
                if ((other.position - self.position).magnitude() < Rr):
                    return True
                else:
                    return False
            if t >= 0 and t <= 1:
                pos1 = self.prevPosition + (self.position-self.prevPosition) * t
                pos2 = other.prevPosition + (other.position-other.prevPosition) * t
                if ((pos1 - pos2).magnitude() < Rr):
                    return True
                else:
                    return False
    def collisionAction(self, other):
        pass
    def __str__(self):
        return('pos = (' + str(self.position) + '); ' + 'vel = (' + str(self.velocity) + '); ' + 'acc = (' + str(self.acceleration) + '); ' + 'aPos = (' + str(self.anglePos) + '); ' + 'aVel = (' + str(self.angleVel) + '); ' + 'aAcc = (' + str(self.angleAcc) + ');')
    def draw(self, window, FPVObj, scale = 1):
        drawV0 = pygame.Vector2(SCREENX/2, SCREENY/2)
        drawM0 = (self.position - FPVObj.position) * scale
        drawPos = drawV0 + drawM0.rotate_rad(-FPVObj.anglePos)
        drawAngle = self.anglePos - FPVObj.anglePos
        return drawPos, drawAngle
    def getNewObjects(self):
        return self.newObjects
    def clearNewObjects(self):
        self.newObjects = []

class Ball(PhysObject):
    def __init__(self):
        super().__init__()
        self.color = pygame.Color(255, 255, 255, 255)
    def draw(self, window, FPVObj = PhysObject(), scale = 1):
        drawPos, drawAngle = super().draw(window, FPVObj, scale)
        pygame.draw.circle(window, self.color, drawPos, self.collisionR * scale, width = 0)
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
        self.acceleration = pygame.Vector2(ax, ay).rotate_rad(self.anglePos)
        super().dT(dt, keys)
    def collisionAction(self, other):
        self.collisionR += 5

class Bullet(PhysObject):
    def __init__(self, pos = pygame.Vector2(), vel = pygame.Vector2(), owner = any):
        super().__init__()
        self.lifetime = 2.0
        self.visionR = 10
        self.collisionR = 5
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(vel)
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
        drawPos, drawAngle = super().draw(window, FPVObj, scale)
        pygame.draw.circle(window, self.color, drawPos, self.visionR * scale, width = 0)
    def dT(self, dt, keys):
        super().dT(dt, keys)
        self.lifetime -= dt
        if self.lifetime <= 0: self.exist = False

class Gun(ActiveBall):
    def __init__(self):
        super().__init__()
    def dT(self, dt, keys):
        super().dT(dt, keys)
        if (keys[pygame.K_SPACE]): self.newObjects.append(Bullet(self.position, self.velocity+pygame.Vector2(0, -1000).rotate_rad(self.anglePos), self))
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
    
def init_window():
    global window, clock
    pygame.init()
    window = pygame.display.set_mode((SCREENX, SCREENY))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Star Wars')
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
 
def init_map():
    global FPVObject, gameMap
    gameMap = Map()
    obj = Gun()
    obj.setPos(pygame.Vector2(0, 0))
    obj.setR(20)
    FPVObject = obj
    gameMap.addObject(obj)
    obj = Ball()
    obj.setPos(pygame.Vector2(50, 50))
    obj.setAcc(pygame.Vector2(1, 1))
    obj.setR(10)
    gameMap.addObject(obj)
    obj = Ball()
    obj.setPos(pygame.Vector2(150, 150))
    obj.setAcc(pygame.Vector2(0, 1))
    obj.setR(10)
    gameMap.addObject(obj)
    obj = Ball()
    obj.setPos(pygame.Vector2(250, 250))
    obj.setAcc(pygame.Vector2(1, 0))
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    screenScale *= 1.25
                if event.button == 5:
                    screenScale *= 0.8
            if event.type == pygame.MOUSEMOTION:
                FPVObject.anglePos += 1.0*event.rel[0]*0.002
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        dt = pygame.time.get_ticks() - clk
        clk = pygame.time.get_ticks()
        window.fill((0, 0, 0, 0))
        gameMap.dT(1.0*dt*0.001, keys)
        gameMap.collision()
        gameMap.addNewObjects()
        gameMap.cleanObj()
        gameMap.draw(window, FPVObject, screenScale)
        pygame.display.flip()
 
if __name__ == '__main__': 
    try:
        main()
    finally:
        pygame.quit()
        sys.exit()