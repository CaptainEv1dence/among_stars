# coding: utf-8
# license: GPLv3
import visual
import objects
from numpy import arctan, cos, sin, arccos
from math import atan2 as atan2
from math import asin as asin

gravitational_constant = 6.67408E-11
Mf = mass_lost_for_tick = 1E5
Vf = initial_fuel_speed = 1E6

"""Гравитационная постоянная Ньютона G"""


def calculate_force(body, space_objects):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    body.Fx = body.Fy = 0
    for obj in space_objects:
        if body == obj:
            continue  # тело не действует гравитационной силой на само себя!
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        r = max(r, body.R + obj.R) # и так сойдет
        an = (1 - 2 * (body.y >= obj.y)) * arccos((obj.x - body.x) / r)
        body.Fx += cos(an) * gravitational_constant * obj.m * body.m / r**2
        body.Fy += sin(an) * gravitational_constant * obj.m * body.m / r**2

        if body.type == "Starship" and body.thrusters_on == 1:
            body.Fx += cos(body.angle) * Mf * Vf
            body.Fy -= sin(body.angle) * Mf * Vf
            body.Fuel -= 0.1
            body.m -= 0.1 * Mf

def move_space_object(body, dt):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """


    ax = body.Fx / body.m
    body.Vx += ax * dt
    body.x += body.Vx * dt + ax * dt * dt / 2



    ay = body.Fy / body.m
    body.y += body.Vy * dt + ay * dt * dt / 2
    body.Vy += ay * dt


def recalculate_space_objects_positions(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """
    for body in space_objects:
        calculate_force(body, space_objects)
    for body in space_objects:
        move_space_object(body, dt)

def collision(body1, body2):
    """
    """

    x1 = visual.scale_x(body1.x)
    x2 = visual.scale_x(body2.x)
    y1 = visual.scale_y(body1.y)
    y2 = visual.scale_y(body2.y)

    if (body1.type == 'Lazer_beam' and body2.type != 'Lazer_beam'):
        body2.HP -= 1
        return [0, 1]
    elif (body2.type == 'Lazer_beam' and body1.type != 'Lazer_beam'):
        body1.HP -= 1
        return [1, 0]
    elif (body1.type!= 'Lazer_beam' and body1.type!= 'Lazer_beam') and (((x1 - x2)**2 + (y1 - y2)**2)**0.5 <= body1.R + body2.R) and (x1 != x2 and y1 != y2):
        body1.HP -= objects.HPCONST * body1.m * body1.m/(body1.m + body2.m)
        body2.HP -= objects.HPCONST * body1.m * body2.m/(body1.m + body2.m)
        k1 = body2.m/(body1.m + body2.m)
        k2 = body1.m/(body1.m + body2.m)
        v1 = (body1.Vx**2 + body1.Vy**2)**0.5
        v2 = (body2.Vx**2 + body2.Vy**2)**0.5
        an = atan2((y2 - y1),(x2 - x1))
        #if ((x - x_s) ** 2 + (y - y_s) ** 2) ** 0.5 == 0:
        #    self.angle = 0
        #else:
        #    self.angle = ( 2 * (y >= y_s) - 1) * acos((x_s - x) / ((x - x_s) ** 2 + (y - y_s) ** 2) ** 0.5)
        #
        an1 = atan2(y1,x1)
        an2 = atan2(y2,x2)
        v_y1 = v1*sin(an + an1)
        v_x1 = (2*(body1.m >= body2.m) - 1)*k1*v1*cos(an + an1)
        v_y2 = v2*sin(an + an2)
        v_x2 = (2*(body2.m >= body1.m) - 1)*k2*v2*cos(an + an2)
        v_11 = (v_x1**2 + v_y1**2)**0.5
        v_22 = (v_x2**2 + v_y2**2)**0.5
        an11 = asin(v_y1/v_11) - an
        an22 = asin(v_y2/v_22) - an
        body1.Vx = v_11*cos(an11)
        body1.Vy = v_11*sin(an11)
        body2.Vx = v_22*cos(an22)
        body2.Vy = v_22*sin(an22)
        return [1, 1]
    else:
        return [0, 0]
if __name__ == "__main__":
    print("This module is not for direct call!")
