# coding: utf-8
# license: GPLv3

import pygame as pg
from math import sin, cos, tan as sin, cos, tan
from math import pi as pi
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

        screen.blit()
        screen.update()
        pg.display.update()


class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surface):
        '''рисует круглый объект на заданной поверхности, 
        используя параметры объекта: радиус, цвет, местоположение'''
        pg.draw.circle(surface, self.obj.color, (scale_x(self.obj.x), scale_y(self.obj.y)), self.obj.R)

    def draw_starship(self, surface):

        an0 = 2 * pi / 9

        r1 = self.obj.R / sin(an0 / 2)
        r2 = self.obj.R / sin((pi - an0) / 2)
        an1 = 3 * pi / 4 - an0/4

        angle = self.obj.angle

        an2 = an1 + self.obj.angle
        an3 = an1 - self.obj.angle

        x = scale_x(self.obj.x)
        y = scale_y(self.obj.y)

        pg.draw.circle(surface, self.obj.color, (x, y), self.obj.R)

        pg.draw.polygon(surface, self.obj.color, [(x + r1 * cos(angle), y + r2 * sin(angle)),
                     (x + r2 * cos(an2), y + r2 * sin(an2)), (x + r2 * cos(an3), y + r2 * sin(an3))])

