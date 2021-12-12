# coding: utf-8
# license: GPLv3
from math import sin, cos, acos, tan, pi as sin, cos, atan, acos, tan, pi
import visual

#consts
HPCONST = 1.0
M_FUEL = 1.0
M_ENERGY = 1.0


class CelestialBody:

    def __init__(self, type, R, color, m, x, y, Vx, Vy):
        self.type = type
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Fx = 0.0
        self.Fy = 0.0
        self.Vx = float(Vx)
        self.Vy = float(Vy)
        self.HP = float(m) * HPCONST


class Star(CelestialBody):
    def __init__(self, m,x,y,Vx,Vy,R,color):
        self.type = 'Star'
        self.R = int(R)
        self.color = color
        self.m = float(m)
        self.x = float(x)
        self.y = float(y)
        self.Fx = 0.0
        self.Fy = 0.0
        self.Vx = float(Vx)
        self.Vy = float(Vy)
        self.HP = float(self.m) * HPCONST
        self.windtimer = 1e7


    def vento_stellare(self):
        return None

    def esplosione_grande(self):
        return None

class DeathStar(CelestialBody):
    def __init__(self, m,x,y,Vx,Vy,R,color):
        self.type = 'DeathStar'
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = float(self.m) * 100 * HPCONST

        self.shottimer = 1e9

    def shot(self):
        return None

class Planet(CelestialBody):
    def __init__(self, m,x,y,Vx,Vy,R,color):
        self.type = 'Planet'
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = float(self.m) * HPCONST

    def esplosione_grande(self):
        return None

class Kikorik(Planet):
    def __init__(self, m,x,y,Vx,Vy,R,color):
        self.type = 'Kikorik'
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = float(self.m) * HPCONST

        self.rocket_timer = 1e5

    def rocket_strike(self):
        return None

class Lazer_beam(Planet):
    def __init__(self, x, y, Vx, Vy):
        self.type = 'Lazer_beam'
        self.m = 0
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = 1
        self.color =(255, 255, 255)
        
class Rocket(Planet):
    def __init__(self, m,x,y,Vx,Vy,R,color):
        self.type = 'Rocket'
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = float(self.m) * HPCONST

        self.Fuel = 10.0

class Entity(CelestialBody):
    None

class Starship(Entity):
    def __init__(self,type, m,x,y,Vx,Vy,R,color):
        self.type = type
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = float(self.m) * HPCONST

        self.Energy = 100.0
        self.Fuel = 100.0
        self.fuel_tanks = 0
        self.batteries = 0
        self.angle = 0
        self.thrusters_on = 0
        self.lazers_on = 0

    def esplosione_grande(self):
        return

    def ejection(self):
        self.m -= self.fuel_tanks * M_FUEL + self.batteries * M_ENERGY
        self.batteries = 0
        self.fuel_tanks = 0


    def targetting(self, event):

        x = visual.scale_x(self.x)
        y = visual.scale_y(self.y)

        x_s = event[0]
        y_s = event[1]

        if ((x - x_s) ** 2 + (y - y_s) ** 2) ** 0.5 == 0:
            self.angle = 0
        else:
            self.angle = ( 2 * (y >= y_s) - 1) * acos((x_s - x) / ((x - x_s) ** 2 + (y - y_s) ** 2) ** 0.5)


    def thrusters_on(self, event):
        self.thrusters_on = 1

    def thrusters_off(self, event):
        self.thrusters_on = 0


class Bonus(Entity):
    None
class Fuel(Entity):
    None

class ShipUpgrade(Entity):
    None
class Energy(Entity):
    None
