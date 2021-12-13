# coding: utf-8
# license: GPLv3

import pygame as pg
import objects
import os
from math import sin, cos, tan as sin, cos, tan
from numpy import pi as pi
"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 1000
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = 1
"""Масштабирование экранных координат по отношению к физическим.

Тип: float

Мера: количество пикселей на один метр."""




def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor
    scale_factor = 0.4 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """

    return int(x * scale_factor) + window_width // 2


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """

    return int(y * scale_factor) + window_height // 2


if __name__ == "__main__":
    print("This module is not for direct call!")


class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, figures, screen):
        '''обновляет экран: заполняет его белым цветом, 
        рисует все объекты из заданного массива'''
        self.screen.fill((0, 0, 0))
        for figure in figures:
            if figure.obj.type == "Starship":
                figure.draw_starship(self.screen)
            else:
                figure.draw(self.screen)
            if figure.obj.type != 'CelestialBody' and figure.obj.type != 'Lazer_beam':
                figure.draw_hp(self.screen)
        screen.blit()
        screen.update()
        pg.display.update()

#self.image = starship_img = pg.image.load(os.path.join(r'C:\Users\petrk\among_stars\img', 'rock.png')).convert()
        #self.image.set_colorkey((0, 0, 0))
        #self.rect = self.image.get_rect()
        #self.rect.center = (300, 300)
class DrawableObject(pg.sprite.Sprite):
    def __init__(self, obj):
        self.obj = obj


    def draw(self, surface):
        '''рисует круглый объект на заданной поверхности, 
        используя параметры объекта: радиус, цвет, местоположение'''
        pg.draw.circle(surface, self.obj.color, (scale_x(self.obj.x), scale_y(self.obj.y)), self.obj.R)

    def draw_hp(self, surface):
        R = self.obj.R
        x = scale_x(self.obj.x)
        y = scale_y(self.obj.y)
        pg.draw.rect(surface, (0, 255, 0),[x - R, y - R - 5, 2*R * (self.obj.HP/ (40 * R**2)), 3])

    def draw_starship(self, surface):

        w = 6
        pi = 3.14159

        an0 = 2 * pi / 9

        r = self.obj.R
        r2 = self.obj.R / sin((pi - an0) / 2)
        an1 = 3 * pi / 4 - an0/4

        angle = self.obj.angle

        an2 = an1 + self.obj.angle
        an3 = an1 - self.obj.angle

        x = scale_x(self.obj.x)
        y = scale_y(self.obj.y)

        #hitbox
        pg.draw.circle(surface, self.obj.color, (x, y), self.obj.R)


        #visual body
        #pg.draw.polygon(surface, self.obj.color, [(x + 2 * r * cos(angle), y + 2 * r * sin(angle)),
         #            (x - r * cos(angle) + w * cos(angle + pi/2), y - r * sin(angle) + w * sin(angle + pi/2)),
          #           (x - r * cos(angle) + w * cos(angle - pi/2), y - r * sin(angle) + w * sin(angle - pi/2))])
        #pg.draw.polygon(surface, self.obj.color, [(x + 10, y ),
        #                     (x - 10.232323, y + 10),
        #                     (x - 10, y - 10)])

        #thruster
        #k = 0.1
        #tr_h = 10
        #tr_w = 3
        #pg.draw.polygon(surface, (255,0,0), [(x, y),
        #                                     (x + tr_h * cos(self.obj.angle + 3*pi/4), y + tr_h * sin(self.obj.angle + 3*pi/4) ),
        #                                     (x + tr_h * cos(self.obj.angle - 3*pi/4), y + tr_h * sin(self.obj.angle - 3*pi/4) )])
