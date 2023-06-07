import pygame






class vector(object):
    def __init__(self, x = 0, y = 0):
        self.Xpos = x
        self.Ypos = y
    def setXY(self, x = 0, y = 0):
        self.Xpos = x
        self.Ypos = y
    def __add__(self, other):
        self.Xpos += other.Xpos
        self.Ypos += other.Ypos
    def __sub__(self, other):
        self.Xpos -= other.Xpos
        self.Ypos -= other.Ypos
    def __mul__(self, other):
        self.Xpos *= other
        self.Ypos *= other
    def __pow__(self, other):
        return (self.Xpos*other.Xpos + self.Ypos*other.Ypos)
    def __truediv__(self, other):
        self.Xpos /= other.Xpos
        self.Ypos /= other.Ypos
    def __abs__(self):
        return ((self.Xpos**2 + self.Ypos**2)**0.5)
    def __str__(self):
        return('x = ' + str(self.Xpos) + '; y = ' + str(self.Ypos) + ';')

class Object(object):
    def __init__(self):
        self.position = vector()
        self.velocity = vector()
        self.acceleration = vector()
        self.anglePos = 0
        self.angleVel = 0
        self.angleAcc = 0
        self.colisionR = 0
    def setPos(self, pos = vector(), angle = 0):
        self.position = pos
        self.anglePos = angle
    def setVel(self, vel = vector(), angle = 0):
        self.velocity = vel
        self.angleVel = angle
    def setAcc(self, acc = vector(), angle = 0):
        self.acceleration = acc
        self.angleAcc = angle
    def setR(self, R = 0):
        self.colisionR = R
    def dPos(self, dPosition = vector(), dA = 0):
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


