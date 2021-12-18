# coding: utf-8 
# license: GPLv3

from objects import Star, Planet, CelestialBody, Starship, DeathStar
from visual import DrawableObject

def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем

            object_type = line.split()[0]
            if object_type == "Star":
                star = CelestialBody(**parse_object_parameters(line))
                objects.append(star)
            elif object_type == "Planet":
                planet = CelestialBody(**parse_object_parameters(line))
                objects.append(planet)
            elif object_type == "Starship":
                starship = Starship(**parse_object_parameters(line))
                objects.append(starship)
            elif object_type == "Kikorik":
                kikorik = CelestialBody(**parse_object_parameters(line))
                objects.append(kikorik)
            elif object_type == "DeathStar":
                ded = DeathStar(**parse_object_parameters(line))
                objects.append(ded)

            else:
                print("Unknown space object")

    return [DrawableObject(obj) for obj in objects]


def parse_object_parameters(line):
    """Считывает данные о !!звезде из строки.

    Входная строка должна иметь слеюущий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.

    Пример строки:

    !!Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание !!звезды.

    **star** — объект !!звезды.
    """
    s = line.split()
    for i in range (len(s)):
        try:
            s[i] = int(s[i])
        except:
            continue

    pars = {'type' : s[0],
    'R' : float(s[1]),
    'color' : s[2],
    'm' : float(s[3]),
    'x' : float(s[4]),
    'y' : float(s[5]),
    'Vx' : float(s[6]),
    'Vy' : float(s[7])}
    return pars




def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.

    Строки должны иметь следующий формат:

    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла

    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'a') as out_file:
        for obj in space_objects:
            if (obj.obj.type == "Planet"):
                out_file.write(str(obj.obj.x) + ' ' + str(obj.obj.y) + ' ' + str(obj.obj.Vx) + ' ' + str(obj.obj.Vy))
                out_file.write('\n')


if __name__ == "__main__":
    print("This module is not for direct call!")
