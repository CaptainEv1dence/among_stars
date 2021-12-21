# coding: utf-8
# license: GPLv3

import pygame as pg
from visual import *
from phys_model import *
from input import *
from objects import *
import thorpy
import time
import numpy as np
from math import sin as sin
from math import cos as cos
from math import pi as pi
from random import randint as randint

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""

def music(name):
    """ Функция, отвечающая за воспроизведение музыки.
    """
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()


#music("kopatich.mp3")

def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global displayed_time
    recalculate_space_objects_positions([dr.obj for dr in space_objects], delta)
    model_time += delta


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    """Обработчик события нажатия на кнопку Pause.
    Останавливает циклическое исполнение функции execution.
    """

    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку !Start!.
    Останавливает главную функцию главного модуля.
    """
    global alive
    alive = False


def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global browser
    global model_time

    model_time = 0.0
    in_filename = "one_satellite.txt"
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

def handle_events(events, menu):
    """Функция обработки событий
    """
    k = 0
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for ship in space_objects:
                    if ship.obj.type == "Starship" and ship.obj.Energy > 0.2:
                        ship.obj.lazers_on = 1
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                for ship in space_objects:
                    if ship.obj.type == "Starship":
                        ship.obj.shield_on = 1
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                for ship in space_objects:
                    if ship.obj.type == "Starship":
                            ship.obj.thrusters_on = 1
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            for ship in space_objects:
                if ship.obj.type == "Starship":
                    ship.obj.lazers_on = 0
        elif event.type == pg.MOUSEBUTTONUP and event.button == 3:
                for ship in space_objects:
                    if ship.obj.type == "Starship":
                        ship.obj.shield_on = 0
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                for ship in space_objects:
                    if ship.obj.type == "Starship" :
                            ship.obj.thrusters_on = 0




def slider_to_real(val):
    '''вспомогательная функция счетчика времени
    на вход получает число'''
    return np.exp(5 + val)


def slider_reaction(event):
    '''функция счетчика времени
    на вход получает событие'''
    global time_scale
    time_scale = slider_to_real(event.el.get_value())


def init_ui(screen):
    '''Создаёт объекты графического дизайна библиотеки: окно, холст, фрейм с кнопками, кнопки, таймер'''
    global browser
    slider = thorpy.SliderX(100, (-10, 10), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    box = thorpy.Box(elements=[
        slider,
        button_pause,
        button_stop,
        button_play,
        button_load,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, timer



def main():
    """Главная функция главного модуля.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer

    print('Modelling started!')
    physical_time = 0

    pg.init()
    pg.font.init()
    FONT = pg.freetype.Font("Lobster-Regular.ttf", 18)

    V = 1E6

    width = 1000
    height = 800
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True


    t_music = 2760/2.5
    t_rocket = 0
    t_bonus = 150
    t_b = 0

    music("kopatich.mp3")

    while alive:

        t_b += 1
        if (t_b >= t_bonus):
            space_objects.append(DrawableObject(Bonus_energy((randint(5,995) - 500)/visual.scale_factor, (randint(5, 795) - 400)/visual.scale_factor)))
            space_objects.append(DrawableObject(Bonus_fuel((randint(5,995) - 500)/visual.scale_factor, (randint(5, 795) - 400)/visual.scale_factor)))
            t_b = 0


        t_music -= 1

        if (t_music <= 0):
            music("kopatich.mp3")
            t_music = 2760/2.5

        for k in space_objects:
            x = visual.scale_x(k.obj.x)
            y = visual.scale_y(k.obj.y)
            x1 = k.obj.x
            y1 = k.obj.y
            vx = k.obj.Vx
            vy = k.obj.Vy


            if k.obj.type == "DeathStar":
                if k.obj.amount == 0:
                    k.obj.amount += 4
                    a = k.obj.spawn()
                    if (a[2]!=0):
                        v = a[1]
                        r = a[0]
                        space_objects.append(DrawableObject(Kikorik(1, x1 , y1 - r, 0, 0, 16, (255, 255, 255),1)))
                        space_objects.append(DrawableObject(Kikorik(1, x1 + r*sin(72*pi/180), y1 - r*cos(72*pi/180), 0, 0, 16, (255, 255, 255),2)))
                        space_objects.append(DrawableObject(Kikorik(1, x1 + r*cos(54*pi/180), y1 + r*sin(54*pi/180), 0, 0, 16, (255, 255, 255),3)))
                        space_objects.append(DrawableObject(
                            Kikorik(1, x1 - r * cos(54 * pi / 180), y1 + r * sin(54 * pi / 180), 0, 0, 16, (255, 255, 255),4)))
                        space_objects.append(DrawableObject(
                            Kikorik(1, x1 + r * sin(72 * pi / 180), y1 - r * cos(72 * pi / 180), 0, 0, 16, (255, 255, 255),5)))


            #t_rocket += 1
            #
            #
            #if t_rocket >= 100:
            #    t_rocket = 0
            #    for b in space_objects:
            #        x = visual.scale_x(b.obj.x)
            #        y = visual.scale_y(b.obj.y)
            #        if d.obj.type == "Kikorik":
            #            space_objects.append(DrawableObject(Rocket()))




            for c in space_objects:
                a = collision(k.obj,c.obj)

                if a[2] == 1:
                    if a[0] == 0:
                        space_objects.remove(k)
                    if a[1] == 0:
                        space_objects.remove(c)

            if (x < 0 or x > 1000 or y < 0 or y > 800) and (k.obj.type == "Lazer_beam" or k.obj.type == "Rocket"):
                space_objects.remove(k)

            if not (k.obj.type == "Lazer_beam" or k.obj.type == "Rocket"):
                if (k.obj.HP <= 0):
                    space_objects.remove(k)

        for ship in space_objects:

            if ship.obj.type == "Starship":
                print(ship.obj.Fuel, ship.obj.Energy)

                if ship.obj.shield_on == 1:

                    if (ship.obj.Energy > 0.2):
                        ship.obj.Energy -= 0.2

                if ship.obj.lazers_on == 1:
                    x = ship.obj.x
                    y = ship.obj.y
                    Vx = cos(ship.obj.angle)*V
                    Vy = -sin(ship.obj.angle)*V

                    if (ship.obj.Energy > 0.6):
                        space_objects.append(DrawableObject(Lazer_beam(x,y,Vx,Vy)))
                        ship.obj.Energy -= 0.6

                    if (len(space_objects) >= 150):
                        space_objects.pop(7)

                ship.obj.targetting(pg.mouse.get_pos())
                print(ship.obj.thrusters_on,ship.obj.angle * 180 / pi, len(space_objects))
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()

        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)


        last_time = cur_time
        drawer.update(space_objects, box)
        time.sleep(1.0 / 60)

    print('Modelling finished!')


if __name__ == "__main__":
    main()
