# coding: utf-8
# license: GPLv3

import pygame as pg
import pygame.freetype
import objects
import os
from math import sin, cos, tan as sin, cos, tan
from numpy import pi as pi
"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие гaрафические объекты и перемещающие их на экране, принимают физические координаты.
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

pg.init()
pg.font.init()
font = pg.freetype.Font("Lobster-Regular.ttf", 18)

window_width = 1000
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = 1
"""Масштабирование экранных координат по отношению к физическим.

Тип: float

Мера: количество пикселей на один метр."""
#def background(screen):
 #   back = pygame.image.load('starsky.jpg')
  #  screen.blit(back, (0, 0))

def drawTextCentered(surface,rect_cent,  text, text_size, color):
    """Функция добавляет текст с заданным размером на заданную поверхность.
    """
    text_rect = font.get_rect(text, size = text_size)
    text_rect.center = rect_cent
    font.render_to(surface, text_rect, text, color, size = text_size)


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине.
    """
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

    #back = pygame.image.load('starsky.jpg')
    def update(self, figures, screen):
        """Обновляет экран: заполняет его белым цветом,
        рисует все объекты из заданного массива.
        """
        self.screen.fill((0, 0, 0))
        #back = pygame.image.load('starsky.jpg')
        #screen.blit(back, (0, 0))
        for figure in figures:
            if figure.obj.type == "Starship":

                figure.draw_starship(self.screen)

                pg.draw.rect(self.screen, (0, 150, 150), [0, 700, 300, 100])
                pg.draw.rect(self.screen, (255, 255, 0),[100, 720, figure.obj.Energy * 1.4, 20])
                pg.draw.rect(self.screen, (255, 0, 255), [100, 760, figure.obj.Fuel * 1.4, 20])
                drawTextCentered(self.screen, (50, 730), f"Energy: {int(figure.obj.Energy)}%", 18, (255, 255, 255))
                drawTextCentered(self.screen, (40, 770), f"Fuel: {int(figure.obj.Fuel)}%", 18, (255, 255, 255))
                pygame.display.flip()
                #text_surface, rect = FONT.render(f" {figure.obj.Energy}", (255, 255, 255))
                #screen.blit(text_surface)

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

class DrawableObject:
    def __init__(self, obj):
        self.obj = obj

    def draw(self, surface):
        """Рисует круглый объект на заданной поверхности,
        используя параметры объекта: радиус, цвет, местоположение.
        """
        pg.draw.circle(surface, self.obj.color, (scale_x(self.obj.x), scale_y(self.obj.y)), self.obj.R)

    def draw_hp(self, surface):
        """Функция отображает состояние здоровья (hp) объектов.
        """
        R = self.obj.R
        x = scale_x(self.obj.x)
        y = scale_y(self.obj.y)
        pg.draw.rect(surface, (0, 255, 0),[x - R, y - R - 5, 2*R * (self.obj.HP/ (40 * R**2)), 3])

    def draw_starship(self, surface):
        """Функция прорисовки космического корабля.
        """
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

        if (self.obj.shield_on == 1):
            pg.draw.circle(surface, (255, 255, 255), (x,y), self.obj.R_sh, 1)

        #hitbox
        pg.draw.circle(surface, self.obj.color, (x, y), self.obj.R, 2)

