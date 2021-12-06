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
    '''функция обработки событий'''
    k = 0
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                k += 1
                for ship in space_objects:
                    if ship.obj.type == "Starship" :
                        if k - k//2 == 1:
                            ship.obj.thrusters_on = 1
                        elif k - k//2 != 1:
                            ship.obj.thrusters_on = 0
        elif event.type == pg.KEYUP:
            if event.key == pg.K_q:
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

    width = 1000
    height = 800
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    while alive:
        for ship in space_objects:
            if ship.obj.type == "Starship":
                ship.obj.targetting(pg.mouse.get_pos())
                print(ship.obj.thrusters_on,ship.obj.angle * 180 / pi)
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
