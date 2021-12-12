# coding: utf-8
# license: GPLv3

from numpy import arctan, cos, sin, arccos

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
            body.Fy += sin(body.angle) * Mf * Vf
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
    if (((body1.x - body2.x)**2 + (body1.y - body2.y)**2)**0.5 <= body1.R + body2.R):
        k1 = body2.m/(body1.m + body2.m)
        k2 = body1.m/(body1.m + body2.m)
        v1 = (body1.vx**2 + body1.vy**2)^0.5
        v2 = (body2.vx**2 + body2.vy**2)^0.5
        an = atan((body2.y - body1.y)/(body2.x - body1.x))
        an1 = atan(body1.y/body1.x)
        an2 = atan(body2.y/body2.x)
        v_y1 = v1*sin(an + an1)
        v_x1 = -k1*v1*cos(an + an1)
        v_y2 = v2*sin(an + an2)
        v_x2 = -k2*v2*cos(an + an2)
        v_11 = (v_x1**2 + v_y1**2)^0.5 
        v_22 = (v_x2**2 + v_y2**2)^0.5
        an11 = asin(v_y1/v_11) - an
        an22 = asin(v_y2/v_22) - an
        body1.vx = v_11*cos(an11)
        body1.vy = v_11*sin(an11)
        body2.vx = v_22*cos(an22)
        body2.vy = v_22*sin(an22)
        
if __name__ == "__main__":
    print("This module is not for direct call!")
