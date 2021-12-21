# coding: utf-8
# license: GPLv3
from math import sin, cos, acos, tan, pi as sin, cos, atan, acos, tan, pi
import visual

#consts
G = gravitational_constant = 6.67408E-11
HPCONST = 1E-22/5.974
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
        self.HP = 40 * self.R ** 2



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
        self.HP = 40 * self.R ** 2
        self.windtimer = 1e7


    def vento_stellare(self):
        return None

    def esplosione_grande(self):
        return None

class DeathStar(CelestialBody):
    def __init__(self,type, m,x,y,Vx,Vy,R,color):
        self.type = "DeathStar"
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.color = color
        self.HP = 40 * self.R ** 2
        self.amount = 0

        self.shottimer = 1e9

    def shot(self):
        return None

    def spawn(self):
        Rk = self.R/visual.scale_factor
        V = (G * self.m / (2 * Rk)) ** 0.5
        return (2 * Rk, V, 4)




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
        self.HP = 40 * self.R ** 2

    def esplosione_grande(self):
        return None

class Kikorik(Planet):
    def __init__(self, m,x,y,Vx,Vy,R,color, number):
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
        self.HP = 40 * self.R ** 2

        self.rocket_timer = 1e5
        self.number = number
    def rocket_strike(self):
        return None

    
class Bullet:
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


class Lazer_beam(Bullet):
    def __init__(self, x, y, Vx, Vy):
        self.type = 'Lazer_beam'
        self.m = 1E-3
        self.x = float(x)
        self.y = float(y)
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = 1
        self.color = (255, 255, 255)

class Rocket(Bullet):
    def __init__(self, x,y,Vx,Vy):
        self.type = 'Rocket'
        self.m = 1
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = 3
        self.color = (255, 0, 0)


        self.Fuel = 10.0

class Entity(CelestialBody):
    None

class Starship(Entity):
    def __init__(self,type, m,x,y,Vx,Vy,R,color):
        self.type = "Starship"
        self.m = m
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = Vx
        self.Vy = Vy
        self.R = R
        self.R_sh = R + 5
        self.color = color
        self.HP = 40 * self.R ** 2

        self.Energy = 100.0
        self.Fuel = 100.0
        self.fuel_tanks = 0
        self.batteries = 0
        self.angle = 0
        self.thrusters_on = 0
        self.lazers_on = 0
        self.shield_on = 0

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


class Bonus_energy(Planet):
    def __init__(self, x,y):
        self.type = 'Bonus_energy'
        self.m = 1
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = 0
        self.Vy = 0
        self.R = 5
        self.color = (255, 255, 0)
        self.HP = 40 * self.R ** 2

class Bonus_fuel(Planet):
    def __init__(self, x,y):
        self.type = 'Bonus_energy'
        self.m = 1
        self.x = x
        self.y = y
        self.Fx = 0
        self.Fy = 0
        self.Vx = 0
        self.Vy = 0
        self.R = 5
        self.color = (40, 40, 0)
        self.HP = 40 * self.R ** 2


class Fuel(Entity):
    None

class ShipUpgrade(Entity):
    None
class Energy(Entity):
    None
