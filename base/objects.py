# coding: utf-8
# license: GPLv3

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


class Star(CelestialBody):
    def __init__(self, parsed_line):
        self.type = 'Star'
        self.m = parsed_line[3]
        self.x = parsed_line[4]
        self.y = parsed_line[5]
        self.Fx = 0
        self.Fy = 0
        self.Vx = parsed_line[6]
        self.Vy = parsed_line[7]
        self.R = parsed_line[1]
        self.color = parsed_line[2]
        
class Planet(CelestialBody):
    def __init__(self, parsed_line):
        self.type = 'Planet'
        self.m = parsed_line[3]
        self.x = parsed_line[4]
        self.y = parsed_line[5]
        self.Fx = 0
        self.Fy = 0
        self.Vx = parsed_line[6]
        self.Vy = parsed_line[7]
        self.R = parsed_line[1]
        self.color = parsed_line[2]
