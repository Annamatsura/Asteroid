import pygame
_V2 = pygame.math.Vector2
from geo_inter_sections import *
from math import sqrt, floor, sin, cos, pi, atan2
from my_colors import COLORVALUES
from random import randint as randInRange
from random import choice

rr = randInRange


def ri(upper):
    """
    Функция возвращающая случайное число в диапазоне от 0 до upper
    :param upper: верхняя граница
    :return: целое число
    """
    return randInRange(0, upper)


def VecToRadAngle(V):
    """
    Переводит вектор в угол
    :param V: векторное значение
    :return: Тангенс + 0.5pi
    """
    return atan2(V.y, V.x) + 0.5 * pi


def RadAngleToVec(angle):
    """
    Переводит угол в вектор
    :param angle: размер угла
    :return: векторное значение
    """
    return _V2(cos(angle), -sin(angle))


RADIANS_FOR_1DEGREE = 0.0175


def loadSettings(fname):
    """
    Загружает информацию формы из файла
    :param fname: название файла
    :return: None
    """
    with open(fname, 'r') as f:
        data = f.readlines()
        global ASTERCOUNT_LIMIT, LIVES, ASTERSPEED_MIN, ASTERSPEED_MAX, ASTERSIZE_MIN, ASTERSIZE_MAX, \
            LEVEL_WIDTH, LEVEL_HEIGHT, width, height
        ASTERCOUNT_LIMIT = int(data[0])

        ASTERSPEED_MIN = int(data[1])
        ASTERSPEED_MAX = int(data[2])
        ASTERSIZE_MIN = int(data[3])
        ASTERSIZE_MAX = int(data[4])

        width, height = int(data[5]), int(data[6])
        LEVEL_WIDTH, LEVEL_HEIGHT = width - 350, height - 53
        LIVES = int(data[7])


loadSettings("test.txt")
STATISTICS = {'score': 0, 'Bounces': 0, 'Astered': 0, 'Shilded': 0, 'Invinced': 0, 'Damages': 0, 'hits': 0,
              'bulletOutside': 0, 'bulletsAll': 0, 'AsteroidsAll': 0, 'heavy': 3, 'step': 0}


def inc(VAL, amount=1):
    """
                dict(STATICTICS) - сборник статистических счетчиков(колво столкновений, колво попаданий, колво уничтоженных астероидов, колво ранений итд)
    Функция увеличивающая статистический показатель по его имени

    :param VAL: имя статистического показателя
            мождет принимать следующие значения
                    'score':  - счетчик очков
                     'Astered':  - счетчик столкнвоений астероидов
                     'Shilded': - счетчик астеродов отраженных Щитом корабля
                      'Invinced':  - счетчик столкновений отраженных  благодаря активному бонусу неуязвимости
                       'Damages': - счетчик попаданий астероидов в обшивку корабля
                        'hits':  - счетчик попаданий пулей по астероиду
                        'bulletOutside': 0     - счетчик промахнувшихся пуль вылетевших за экран
                        'bulletsAll': 0, - счетчик выпущенных пуль
                        'AsteroidsAll': 0, - сколкько всего астеродиов было порожденно в сумме за время последнего запуска игры
    :param amount: значение на которое он будет увеличен Статистический показатель
    :return: None
    """
    global STATISTICS
    if VAL in STATISTICS:
        STATISTICS[VAL] += amount
    else:
        print('STATISTICS KEY ERROR')


def S_get(VAL):
    """
    Проверка наличия значения в файле
    :param VAL: значение
    :return: значение или ошибка
    """
    global STATISTICS
    if VAL in STATISTICS:
        return STATISTICS[VAL]
    else:
        return '<error: no_such_key in dict STATISTICS>'


AVAILABLECOLORS = COLORVALUES()


def getRandColor():
    """
    Функция, вынимающая случайный цвет из списка цветов
    :return: цвет
    """
    global AVAILABLECOLORS
    maxId = len(AVAILABLECOLORS) - 1
    if (maxId == -1):
        AVAILABLECOLORS = COLORVALUES()

    anycolorId = ri(maxId)
    thecolor = AVAILABLECOLORS[anycolorId]
    del AVAILABLECOLORS[anycolorId]

    return thecolor


# SUPPORT FUNCTIONS
r = round


def rgb(r, g, b):
    """
    Функция возвращающая цвет rgb в привычном для pygame формате
    :param r: red
    :param g: green
    :param b: blue
    :return: tuple rgb
    """
    return (r, g, b)


pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 14)
STATfont = pygame.font.SysFont('Comic Sans MS', 36)


def write(text, color, XY, thefont=myfont, silent=False):
    """
    Функция отрисовывающая на экране строку заданного цвета и в заданном месте
    :param text: строка с текстом
    :param color: цвет текста
    :param XY: координаты на экране
    :param thefont:  (Шрифт) -  экземпляр объект  pygame.font  SysFont
    :return: None
    """
    global window, myfont

    if thefont == None:
        thefont = myfont

    textsurface = thefont.render(str(text), False, (255, 255, 255))
    if not silent:
        window.blit(textsurface, XY)
    if silent:
        return textsurface


# preventive declaration
NOTIFY = ''
pause = None
wait = None
run = None
pressed = None
collided = None
allowCollide = None

pygame.init()

window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def AddNewObj(newobj):
    """
    Добавление объекта в список для дальнейшего ввода
    в игровой уровень
    :param newobj: объект
    :return: None
    """
    global constructors
    constructors.append(newobj)


def DestroyUID(uid):
    """
    Удаление объекта по id
    :param uid: id
    :return: None
    """
    global desructors
    if uid in allObjects.keys():
        ripobj = allObjects[uid]
        ripobj.ignoredByCollider = True
        ripobj.collidesWith = []
        ripobj.event_destroy()
        destructors.add(ripobj)


def DestroyObj(obj):
    """
    Удаление объекта
    :param obj: объект
    :return: None
    """
    DestroyUID(obj.uid)


def same(o1, o2):
    """
    Сравнение типов объектов
    :param o1: первый объект
    :param o2: второй объект
    :return: None
    """
    return o1._is(o2._am())


def distanceBetweenObj(a, b):
    """
    Расстояние между объектами
    :param a: первый объект
    :param b: второй объект
    :return: расстояние
    """
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def distanceBetweenPoints(ax, ay, bx, by):
    """
    Расстояние между точками объектов
    :param ax: 1X
    :param ay: 1Y
    :param bx: 2X
    :param by: 2Y
    :return: расстояние
    """
    return sqrt((bx - ax) ** 2 + (by - ay) ** 2)


# ------------------------------------
#       OBJECT SYSTEM BASIS OBJECT
# ------------------------------------

class PureBasicObject:
    """
    Базовый объект, содержит инициализацию методов,
    использующихся для каждого игрового объекта
    """

    def event_create(self):
        pass

    def ev_react(self, the_event):
        pass

    def move(self):
        pass

    def event_aftermove(self):
        pass

    def event_step(self):
        pass

    def collideWith(self, obj2, dist):
        pass

    def event_afterstep(self):
        pass

    def draw(self):
        pass

    def event_destroy(self):
        pass

    def __str__(self):
        return self._am() + ' ' + str(self.uid)

    def _is(self, who):
        return (who == self.objtype)

    def _am(self):
        return (self.objtype)

    def _xy(self):
        """
        Возвращает tuple текущего x и y
        :return: tuple
        """
        return (self.x, self.y)

    def _collidesWith(self, obj_type):
        return obj_type in self.collidesWith

    def _bouncesWith(self, obj_type):
        return obj_type in self.bouncesWith


class GameObject(PureBasicObject):
    """
     родительский Класс-прототип  для всех игровых объектов
    """

    def __init__(self, x=0, y=0, xspeed=0, yspeed=0, radius=0, color=(255, 255, 255), objtype='undefined',
                 form='circle', borderWidth=4, collidesWith=[], bouncesWith=[]):
        self.collidesWith = collidesWith
        self.bouncesWith = bouncesWith
        self.uid = None
        self.x = x
        self.y = y
        self.xprev, self.yprev = x, y
        self.prevBounces = {}

        self.xspeed = xspeed
        self.yspeed = yspeed

        self.direction = 0
        self.RADdirection = 0
        self.speed = 0

        self.color = color
        self.radius = radius
        self.radius2 = self.radius ** 2
        self.mass = radius

        self.objtype = objtype
        self.form = form
        self.borderWidth = borderWidth

        self.ignoredByCollider = False
        self.leftX, self.rightX = self.x - self.radius, self.x + self.radius
        self.topY, self.lowY = self.y - self.radius, self.y + self.radius
        self.myZones = set()

        cX, cY, R = self.x, self.y, self.radius
        self.dots = {
            'midcenter': (floor(cX), floor(cY)),
            'left': (floor(cX - R), floor(cY)),
            'right': (floor(cX + R), floor(cY)),
            'top': (floor(cX), floor(cY - R)),
            'bottom': (floor(cX), floor(cY + R))
        }
        self.lines = {}

    def dot(self, key):
        if key in self.dots:
            return self.dots[key]
        else:
            print('ERROR. WRONG KEY NAME <' + key + '> Default (x,y) was returned to prevent FAIL')
            return self.drawpoz()

    def update_directionRAD(self, modificator_in_rads):
        self.direction += modificator_in_rads

    def update_directionDEG(self, modificator_in_degrees):

        self.direction += modificator_in_degrees

        if self.direction > 360:  self.direction -= 360
        if self.direction < 0:  self.direction += 360

        self.RADdirection = self.direction / 180 * pi

    def update_speed(self, modificator):
        self.speed += modificator

    def update_VD(self):
        self.update_directionDEG(0)
        newMovementV = RadAngleToVec(self.RADdirection) * self.speed

        self.xspeed, self.yspeed = newMovementV

    def event_create(self):
        """
        Функция вызывающаяся непосредственно в момент добавления
        игрового объекта на локацию
        :return: None
        """
        self.myUidLabel = myfont.render(str(self.uid), False, (255, 255, 255))

    def event_afterstep(self):
        """
        Функция запоминающая координаты предыдущего шага для
        разрешения заедания шаров
        :return: None
        """
        self.xprev, self.yprev = self.x, self.y

    def move(self):
        """
        Функция изменения скорости
        :return: None
        """
        global LEVEL_WIDTH
        self.x += self.xspeed
        self.y += self.yspeed

    def event_aftermove(self):
        """
        Функция перерасчета опорных координат
        участвующих в столкновениях
        :return: None
        """

        self.leftX, self.rightX = self.x - self.radius, self.x + self.radius
        self.topY, self.lowY = self.y - self.radius, self.y + self.radius

        cX, cY, R = self.x, self.y, self.radius

        if self.form == 'circle':
            self.dots = {
                'midcenter': (floor(cX), floor(cY)),
                'midleft': (floor(cX - R), floor(cY)),
                'midright': (floor(cX + R), floor(cY)),
                'midtop': (floor(cX), floor(cY - R)),
                'midbottom': (floor(cX), floor(cY + R))
            }
            self.lines = {
                'A-0-B': (self.dots['midleft'], self.dots['midright']),
                'C-0-D': (self.dots['midtop'], self.dots['midbottom'])
            }

        if self.form == 'triangle':
            x, y = self._xy()
            r = self.radius
            cur_angle = self.RADdirection

            vecForward = RadAngleToVec(cur_angle) * r * 2
            vecLeft = RadAngleToVec(cur_angle + (110 / 180 * pi)) * r
            vecRight = RadAngleToVec(cur_angle - (110 / 180 * pi)) * r

            vecForward = RadAngleToVec(self.RADdirection) * r * 2
            vecLeft = RadAngleToVec(self.RADdirection + (110 / 180 * pi)) * r
            vecRight = RadAngleToVec(self.RADdirection - (110 / 180 * pi)) * r
            vecR1 = RadAngleToVec(self.RADdirection - 0.5 * pi) * r * 1.25
            vecL1 = RadAngleToVec(self.RADdirection + 0.5 * pi) * r * 1.25
            vecL2 = RadAngleToVec(self.RADdirection + (20 / 180 * pi)) * 0.8 * r
            vecR2 = RadAngleToVec(self.RADdirection - (20 / 180 * pi)) * 0.8 * r

            dotA = (x + vecForward.x, y + vecForward.y)
            dotB = (x + vecRight.x, y + vecRight.y)
            dotB2 = (x + vecR2.x, y + vecR2.y)
            dotB3 = (x + vecR1.x, y + vecR1.y)
            dot0 = (x, y)
            dotD = (x + vecLeft.x, y + vecLeft.y)
            dotD2 = (x + vecL2.x, y + vecL2.y)
            dotD3 = (x + vecL1.x, y + vecL1.y)

            dotA = (x + vecForward.x, y + vecForward.y)
            dotB = (x + vecRight.x, y + vecRight.y)
            dotC = (x + vecLeft.x, y + vecLeft.y)
            dot0 = (x, y)

            self.dots = {'A': dotA,
                         'B': dotB,
                         'C': dotC,
                         '0': dot0,
                         'B2': dotB2,
                         'B3': dotB3,
                         'D2': dotD2,
                         'D3': dotD3
                         }

            self.lines = {
                'AB3': (dotA, dotB3),
                'AD3': (dotA, dotD3),
                'B3D3': (dotB3, dotD3),
                '0A': (dot0, dotA),
                '0D3': (dot0, dotD3),
                '0D3': (dot0, dotD3),
            }

    def drawpoz(self):
        """
        Функция округления позиционных координат
        :return: tuple
        """
        return (round(self.x), round(self.y))

    def draw(self):
        """
        Функция, рисующая объекты
        :return: None
        """
        global window

        # CIRCLE
        if self.form == 'circle':

            if self.borderWidth == None:
                pygame.draw.circle(window, self.color, self.drawpoz(), self.radius)
            else:
                pygame.draw.circle(window, self.color, self.drawpoz(), self.radius - self.borderWidth, self.borderWidth)

            if True:  # details for asteroid painting
                if self.objtype == 'Asteroid':
                    pygame.draw.circle(window, (200, 50, 70), self.drawpoz(), self.radius * 10 // 9 - self.borderWidth,
                                       self.borderWidth)
                    write('R' + str(round(self.radius)), (255, 255, 255), self.drawpoz())

        # TRIANGLE
        if self._is('Player') and self.form == 'triangle':
            x, y = self.drawpoz()
            r = self.radius

            vecForward = RadAngleToVec(self.RADdirection) * r * 2
            vecLeft = RadAngleToVec(self.RADdirection + (110 / 180 * pi)) * r
            vecRight = RadAngleToVec(self.RADdirection - (110 / 180 * pi)) * r
            vecR1 = RadAngleToVec(self.RADdirection - 0.5 * pi) * r * 1.25
            vecL1 = RadAngleToVec(self.RADdirection + 0.5 * pi) * r * 1.25
            vecL2 = RadAngleToVec(self.RADdirection + (20 / 180 * pi)) * 0.8 * r
            vecR2 = RadAngleToVec(self.RADdirection - (20 / 180 * pi)) * 0.8 * r

            dotA = (x + vecForward.x, y + vecForward.y)
            dotB = (x + vecRight.x, y + vecRight.y)
            dotB2 = (x + vecR2.x, y + vecR2.y)
            dotB3 = (x + vecR1.x, y + vecR1.y)
            dot0 = (x, y)
            dotD = (x + vecLeft.x, y + vecLeft.y)
            dotD2 = (x + vecL2.x, y + vecL2.y)
            dotD3 = (x + vecL1.x, y + vecL1.y)

            pygame.draw.circle(window, self.color, dotA, 7)
            pygame.draw.circle(window, self.color, dotD, 7)
            pygame.draw.circle(window, self.color, dotB, 7)

            pygame.draw.polygon(window, rgb(0, 60, 60), [dotD, dotD2, dotA, dotB2, dotB])
            pygame.draw.polygon(window, rgb(200, 30, 30), [dotD, dotD3, dotD2, dotA, dotB2, dotB3, dotB, dot0])
            pygame.draw.polygon(window, rgb(162, 133, 236), [dotD, dotA, dotB, dot0])
            pygame.draw.polygon(window, rgb(145, 115, 219), [dotD, dotA, dot0])
            pygame.draw.polygon(window, rgb(111, 93, 162), [dotD, dotA, dotB, dot0], 9)
            pygame.draw.polygon(window, rgb(250, 140, 200), [dotD, dot0, dotB])

            val = 100 + round(120 * abs(self.speed) / self.engine_max)
            pygame.draw.circle(window, (30 + val, 30 + val, 30 + val), dotA, 3)
            pygame.draw.circle(window, (30 + val, 30 + val, 30 + val), dotB, 3)
            pygame.draw.circle(window, (30, 30 + val, 30), dotB2, 3)
            pygame.draw.circle(window, (30, 30 + val, 30 + val), dotB3, 3)
            pygame.draw.circle(window, (30 + val, 30 + val, 30 + val), dotD, 3)
            pygame.draw.circle(window, (30, 30 + val, 30), dotD2, 3)
            pygame.draw.circle(window, (30, 30 + val, 30 + val), dotD3, 3)
            pygame.draw.circle(window, (30, 30 + val, 30), dot0, 3)

            write(str(self.direction), (255, 255, 255), dotA)


#       GAMEWORLD STEPWAY ROUTINES
# ------------------------------------

def MoveAll():
    """
    Функция которая вызывает obj.event_move для каждого объекта из списка
    :return: None
    """
    global allObjects
    for obj in allObjects.values():
        obj.move()


def AfterMoveAll():
    """
    Функция которая вызывает obj.event_aftermove для каждого объекта из списка
    :return: None
    """
    global allObjects
    for obj in allObjects.values():
        obj.event_aftermove()


def StepAll():
    """
    Функция которая вызывает obj.event_step() для каждого объекта из списка
    :return: None
    """
    global allObjects
    for obj in allObjects.values():
        obj.event_step()


def AfterStepAll():
    """
    Функция которая вызывает obj.after_step() для каждого объекта из списка
    :return: None
    """
    global allObjects
    for obj in allObjects.values():
        obj.event_afterstep()


def ResetTree():
    """
    Функция для работы с квадродеревьями
    Отрубает под корень всю систему и наращивает заново дерево
    :return: None
    """
    global Root
    global Leaves
    global allObjects
    del Leaves
    Root.freeAll
    del Root

    Leaves = set()  # this is set of unique values that are store each of them only in one and only one exmplaire

    Root = Node([0, 0, LEVEL_WIDTH, LEVEL_HEIGHT], None, 'R', [], Leaves, S_get('step'))
    Root.objects = list(allObjects.values())
    Leaves.add(Root)
    for obj in allObjects.values():
        obj.myZones = set()
    Root.divide()

    if pygame.key.get_pressed()[pygame.K_u]:
        print('step=', STATISTICS['step'])
        Root.investigate()
        print('step=', STATISTICS['step'])


def CollideAll():
    """
    Проверка столкновений зонах и вызов реакций
    у заинтересованных в этом объектах
    :return: None
    """
    ResetTree()
    global Leaves
    global wait, pause

    inform = pygame.key.get_pressed()[pygame.K_i]
    donePairs = []
    for zone in Leaves:
        if len(zone.objects) <= 1:
            continue

        for obj1 in zone.objects:
            if obj1.ignoredByCollider:
                continue

            for obj2 in zone.objects:

                if obj2.ignoredByCollider:
                    continue

                if (obj1.uid == obj2.uid):
                    continue

                pair = {obj1.uid, obj2.uid}
                if pair in reversed(donePairs):
                    continue
                else:
                    donePairs.append(pair)

                o1 = obj1._am()
                o2 = obj2._am()

                a_reacts = obj1._collidesWith(o2)
                b_reacts = obj2._collidesWith(o1)

                if (not a_reacts and not b_reacts): continue

                touched = False
                geom = {obj1.form, obj2.form}
                if geom == {'circle'}:
                    d = distanceBetweenObj(obj1, obj2)
                    rrsum = obj1.radius + obj2.radius - 2
                    touched = (d < rrsum)

                if geom == {'circle', 'triangle'}:

                    ok = obj1.form == 'triangle'
                    triang, circ = (obj1, obj2) if ok else (obj2, obj1)

                    for lineTriang in triang.lines.values():
                        touched |= line_x_circle(lineTriang, circ._xy(), circ.radius)
                        if touched:
                            #
                            d = distanceBetweenObj(obj1, obj2)
                            rrsum = obj1.radius + obj2.radius - 2
                            break

                if geom == {'rectangle', 'triangle'}:
                    for lineO1 in obj1.lines.values():
                        for lineO2 in obj1.lines.values():
                            touched |= line_x_line(lineO1, lineO2)
                            if touched:
                                break

                if touched:

                    if inform:  print(o1, o2, obj1.uid, obj2.uid, 'pair collided ')

                    if a_reacts:
                        obj1.collideWith(obj2, d)

                    if b_reacts:
                        obj2.collideWith(obj1, d)

                    a_bounces = obj1._bouncesWith(obj2._am())
                    b_bounces = obj2._bouncesWith(obj1._am())
                    if a_bounces or b_bounces:
                        SolveTheCollidement(obj1, obj2, a_bounces, b_bounces, d, rrsum)

                else:
                    if inform:
                        print(o1, o2, obj1.uid, obj2.uid, 'pair too far ', d, ' > ', rrsum)


def ReactEventsAll(events, pressed):
    """
    Заставляет все объекты прореагировать на события
    :param events: Список событий pygame
    :return: None
    """
    for event in events:
        LevelBrains.ev_react(event)

    for obj in allObjects.values():
        if obj == LevelBrains:
            continue

        for event in events:
            obj.ev_react(event)


def draw_uproots(owner):
    """
    Рисует все зоны дерева
    :param owner: Зона Root
    :return: None
    """
    if owner == None:
        return
    for zone in owner.subzones:
        pygame.draw.rect(window, zone.playerIn, (zone.leftX, zone.topY, zone.width, zone.height), 1)
        draw_uproots(zone)


def DrawLeaves():
    """
    Рисует периферийные зоны
    :return: None
    """
    global window
    global Root, Leaves

    if True or pygame.key.get_pressed()[pygame.K_z]:
        draw_uproots(Root)

    if False or pygame.key.get_pressed()[pygame.K_x]:
        for zone in Leaves:
            pygame.draw.rect(window, zone.playerIn, (zone.leftX, zone.topY, zone.width, zone.height), 1)


def DrawAll():
    """
    Отчищает холст, отрисовывает объекты, отрисовывает зоны и
    выводит холст на экран
    :return:
    """
    global window
    global allObjects
    window.fill((4, 9, 15))
    for obj in allObjects.values():
        obj.draw()

    DrawLeaves()

    global STATISTICS, pause, Leaves
    x = LEVEL_WIDTH + 5
    y = 3
    if True or pygame.key.get_pressed()[pygame.K_p]:
        for key, val in STATISTICS.items():
            txt = str(key) + ': ' + str(val)
            write(txt, (255, 255, 255), (x, y), STATfont)
            y += 55
    write('objs:' + str(len(allObjects)), (255, 255, 255), (x, y), STATfont)
    y += 55
    write('Leaves:' + str(len(Leaves)), (255, 255, 255), (x, y), STATfont)

    write(NOTIFY, (255, 255, 255), (10, 720), STATfont)

    pygame.display.flip()


def Update():
    """
    Вводит в игровой уровень объекты из списка на добавление
    И выводит из игрового оборота объекты, которые были помечены
    на удаление (были добавлены в destructors set)
    :return: None
    """
    global constructors, destructors, allObjects, uid

    # BORNS
    while len(constructors) > 0:
        newobj = constructors[0]
        newobj.uid = uid
        allObjects[uid] = newobj

        newobj.event_create()

        del constructors[0]
        uid += 1

    # DIES
    toDelete = list(destructors)
    while len(toDelete) > 0:
        RIPobj = toDelete[0]

        uid = RIPobj.uid
        if uid in allObjects.keys():
            del allObjects[uid]
        else:
            pass
            print('ERROR')

        destructors.remove(RIPobj)
        del toDelete[0]
        del RIPobj


def ClearLevel():
    """
    Очищает игровой уровень:
    Останавливает и очищает очередь к созданию
    Все существующие объекты помечает на уничтожение в конце шага
    :return:
    """
    constructors = []
    print('Starting Destruction')
    destructors = list(allObjects.values())

    print('Freeing memory..')
    Update()
    print('Done.')


def Finalize():
    """
    Вызывает очистку при закрытии программы
    :return: None
    """
    ClearLevel()

    print('Closing Game Environment')
    pygame.quit()
    print('Done')


def PrepareGameLevel():
    """
    Подготавливает первый и единственный игровой уровень
    :return: None
    """
    global constructors
    global LevelBrains

    LevelBrains = LevelController()

    constructors = [
        Player(700, 700),
        LevelBrains

    ]
    constructors.extend([Asteroid() for _ in range(ASTERCOUNT_LIMIT)])


class Bullet(GameObject):
    """
    Класс пули
    """

    def __init__(self, x, y, xspeed=0, yspeed=-5):
        super().__init__(x, y, xspeed, yspeed, 7, rgb(255, 0, 0), 'Bullet', 'circle', None)

        self.collidesWith = ['Asteroid']
        self.power = 1
        self.livetime = 0

    def collideWith(self, obj2, dist=12345):
        """
        Функция действий при столкновении
        :param obj2: объект с которым произошло столкновение
        :return: None
        """
        inc('score',
            3)  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
        self.collidesWith = []

        DestroyObj(self)

    def event_aftermove(self):
        """
        Действия пули после перемещения event_move()
        :return: None
        """
        global LEVEL_WIDTH, LEVEL_HEIGHT

        outside = False
        outside |= self.x < -30
        outside |= self.x > (LEVEL_WIDTH + 30)
        outside |= self.y < -30
        outside |= self.y > (LEVEL_WIDTH + 30)
        if outside:
            inc('bulletOutside')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            DestroyObj(self)
            self.collidesWith = []

            return

        self.livetime += 1
        if self.livetime > 100:
            inc('bulletOutside')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            DestroyObj(self)
            self.collidesWith = []

            return

        super().event_aftermove()


class Shield(GameObject):
    """
    Класс Щит для защиты Player
    """

    def __init__(self, owner):
        super().__init__(owner.x, owner.y, owner.xspeed, owner.yspeed, 39, rgb(22, 222, 76), 'Shield', 'circle', 7)

        self.myOwner = owner
        self.maxradius = 57
        self.minradius = 37
        self.growth = 3

        print('Shilds Up')

    def event_step(self):
        """
        игровая логика щита
        :return: None
        """
        if self.growth > 0:
            if self.radius < self.maxradius:
                self.radius += self.growth
            else:
                self.growth = -1.3
        else:
            if self.radius > self.minradius:
                self.radius += self.growth
            else:
                self.radius = self.minradius

    def event_create(self):
        """
        Добавляет щит в локацию
        :return: None
        """
        super().event_create()
        theplayer = self.myOwner
        theplayer.myshield = self.uid

        self.x = self.myOwner.x
        self.y = self.myOwner.y
        self.xspeed = self.myOwner.xspeed
        self.yspeed = self.myOwner.yspeed

    def event_destroy(self):
        """
        Удаляет щит
        :return:
        """
        self.myOwner.myshiled = None

    def event_aftermove(self):
        """
        Действия после столкновения
        :return: None
        """
        self.x = self.myOwner.x
        self.y = self.myOwner.y
        self.xspeed = self.myOwner.xspeed
        self.yspeed = self.myOwner.yspeed
        self.myOwner.hp -= 0.7
        super().event_aftermove()


class Bouncer(GameObject):
    """
    Класс Bouncer для демонстрации отталкивания астероидов
    от различного веса
    """

    def __init__(self, x, y, xspeed=0, yspeed=-5, mass=20):
        density = min(255, mass)
        super().__init__(x, y, xspeed, yspeed, 7, rgb(density, 125, 219), 'Bouncer', 'circle', None)

        self.collidesWith = ['Asteroid']
        self.bouncesWith = ['Asteroid']
        self.power = 1
        self.livetime = 0
        self.mass = mass
        self.massPICTURE = write('MM' + str(self.mass), (255, 255, 255), (0, 0), thefont=None, silent=True)

    def draw(self):
        global window
        super().draw()

        window.blit(self.massPICTURE, (self.x + 5, self.y - 10))

    def collideWith(self, obj2, dist=12345):
        pass

    def event_aftermove(self):

        global LEVEL_WIDTH, LEVEL_HEIGHT

        outside = False
        outside |= self.x < -30
        outside |= self.x > (LEVEL_WIDTH + 30)
        outside |= self.y < -30
        outside |= self.y > (LEVEL_WIDTH + 30)
        if outside:
            inc('bulletOutside')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            DestroyObj(self)
            self.collidesWith = []

            return

        self.livetime += 1
        if self.livetime > 100:
            inc('bulletOutside')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            DestroyObj(self)
            self.collidesWith = []

            return

        super().event_aftermove()


class Asteroid(GameObject):
    """
    Класс Астероид
    """

    def __init__(self, x=None, y=None, radius=None, color=None, xspeed=None,
                 yspeed=None):  # ( x, y , xspeed, yspeed, radius, color , objtype, form='circle', borderWidth=4):

        global LEVEL_WIDTH, LEVEL_HEIGHT
        if x == None:
            x = randInRange(100, LEVEL_WIDTH - 100)

        if y == None:
            y = randInRange(100, LEVEL_HEIGHT - 100)

        global ASTERSPEED_MIN, ASTERSPEED_MAX

        if xspeed == None:
            xspeed = randInRange(ASTERSPEED_MIN, ASTERSPEED_MAX) * choice([-1, +1])
            xspeed = 1 if xspeed == 0 else xspeed
        if yspeed == None:
            yspeed = randInRange(ASTERSPEED_MIN, ASTERSPEED_MAX) * choice([-1, +1])
            yspeed = 1 if yspeed == 0 else yspeed

        global ASTERSIZE_MIN, ASTERSIZE_MAX
        if radius == None:
            radius = randInRange(ASTERSIZE_MIN, ASTERSIZE_MAX)

        if color == None:
            color = randcolor = (ri(255), ri(255), ri(255))
        self.normalsize = radius
        super().__init__(x, y, xspeed, yspeed, 0, color, 'Asteroid', 'circle', rr(3, 7))

        self.collidesWith = ['Asteroid', 'Player', 'Shield', 'Bullet', 'Bouncer']
        self.bouncesWith = ['Asteroid', 'Player', 'Shield', 'Bullet', 'Bouncer']
        self.mass = radius + ri(100)

    def event_create(self):
        """
        Действия при размещении объекта в локации
        :return: None
        """
        inc('AsteroidsAll')

    def event_step(self):
        """
        Действия при первых шагах
        :return: None
        """
        if self.radius < self.normalsize:
            self.radius += 0.2
            self.mass = self.radius
            self.radius2 = self.radius ** 2
        else:
            self.normalsize = 0

        super().event_step()

    def event_aftermove(self):
        """
        Действия после шага
        :return:
        """
        global LEVEL_WIDTH, LEVEL_HEIGHT

        if self.y > LEVEL_HEIGHT:
            self.y = LEVEL_HEIGHT
            self.yspeed = -1 * self.yspeed

        if self.y < 0:
            self.y = 0
            self.yspeed = -1 * self.yspeed

        if self.x > LEVEL_WIDTH:
            self.x = LEVEL_WIDTH
            self.xspeed = -1 * self.xspeed

        if self.x < 0:
            self.x = 0
            self.xspeed = -1 * self.xspeed

        super().event_aftermove()

    def collideWith(self, obj2, dist=12345):
        """
        Действия при столкновении
        :param obj2: объект с которым столкновение
        :return: None
        """
        if obj2._is('Asteroid'):
            inc('Astered')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            # obj2.radius+=0.35

        if obj2._is('Shield'):
            obj2.radius -= 5
            inc('Shilded')  # 'score':0, 'Astered':0, 'Shilded':0, 'Invinced':0,'Damages':0, 'hits':0, 'bulletOutside':0, 'bulletsAll':0
            if self.radius < 15:
                DestroyObj(self)

        if obj2._is('Bullet'):
            inc('hits')
            DestroyObj(obj2)

            self.radius -= 7 + self.radius * 0.05
            if self.radius <= 15:
                DestroyObj(self)

        if obj2._is('Player'):

            p = obj2
            isinvincible = False

            if True or ('invincible' in p.active_bonuses):
                if p.active_bonuses['invincible'] > 0:
                    isinvincible = True
                    inc('Invinced')
                    if self.radius < 10:
                        DestroyObj(self)

            if not isinvincible:
                p.hp -= self.radius
                inc('Damages')
                p.active_bonuses['invincible'] += 150
                print('Ouch, hp=', p.hp)
                global NOTIFY
                NOTIFY = 'Ouch, hp=' + str(round(p.hp, 1))

                self.radius *= 0.98
                self.radius -= 3
                if self.radius < 7:
                    DestroyObj(self)

        def draw(self):
            super().draw()
            write('RR' + str(round(self.radius)), (255, 255, 255), (round(self.x - 9), round(self.y)), STATfont)

            for elm in self.prevBounces.values():
                self.tt += elm
            write('T' + str(round(self.tt)), (255, 255, 255), (round(self.x - 9), round(self.y + 20)), STATfont)


class LevelController(GameObject):

    def event_create(self):
        """
        Создание объекта и его размещение
        :return: None
        """
        super().event_create()
        self.x = -100
        self.y = -100
        self.ignoredByCollider = True

    def ev_react(self, the_event):
        """
        Реакция на нажатие клавиш
        :param the_event: клавиша
        :return: None
        """
        global pause
        global allowCollde

        if the_event.type == pygame.KEYDOWN:

            if the_event.key == pygame.K_ESCAPE:
                global run
                run = False
                print('You are leaving. Bue Bue')

            if the_event.key == pygame.K_p:
                pause = not pause
                print('pause = ', pause)

            if the_event.key == pygame.K_h:
                inc('heavy', 5)

            if the_event.key == pygame.K_j:
                inc('heavy', -5)

            if the_event.key == pygame.K_l:
                inc('heavy', -100)

            if the_event.key == pygame.K_m:
                inc('heavy', 100)

            if the_event.key == pygame.K_r:
                pause = True
                ClearLevel()
                print('Restarting')
                PrepareGameLevel()
                LIVES = 3
                print('unPausing..')
                pause = False

            if the_event.key == pygame.K_F5:
                global allObjects
                for ouid, obj in allObjects.items():
                    if obj._is('Asteroid'):
                        DestroyUID(ouid)
                Update()
                AddNewObj(Asteroid(70, 70, 90, None, 0, 0))
                Update()

            if the_event.key == pygame.K_F12:
                ASTERSPEED_MIN += 1
                ASTERSPEED_MAX += 1
            if the_event.key == pygame.K_F11:
                ASTERSPEED_MIN -= 1
                ASTERSPEED_MAX -= 1

            if the_event.key == pygame.K_F10:
                ASTERSIZE_MIN += 1
                ASTERSIZE_MAX += 5
            if the_event.key == pygame.K_F9:
                ASTERSIZE_MIN -= 1
                ASTERSIZE_MAX -= 5

    def move(self):
        pass

    def event_aftermove(self):
        """
        Действия после перемещения
        :return: None
        """
        super().event_aftermove()


class Timer(GameObject):
    """
    Класс для обратного отсчета времени
    перед выполнением какого-то действия (пеиодичного
    или разового)
    """

    def __init__(self, period=500, curtime=900, action=None, destroyAfter=None):

        super().__init__(-100, -100)
        self.period = period
        self.curtime = curtime
        self.action = action
        self.destroyAfter = destroyAfter

    def event_step(self):
        """
        Метод вызывающейся каждый игровой такт
        после перемещения но перед обработкой столкновений
        для обработки специфической персональной логики
        объекта.
        :return: None
        """
        self.curtime -= 1

        if self.curtime <= 0:
            self.action()

            if self.destroyAfter != None:

                self.destroyAfter -= 1

                if self.destroyAfter < 0:
                    DestroyUID(self.uid)

            else:
                self.curtime = self.period
        else:
            global NOTIFY
            NOTIFY = 'You are dead... Time to Reborn:' + str(self.curtime // 40)


class Player(GameObject):

    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, 30, rgb(255, 255, 0), 'Player', 'triangle', None)

        self.hpmax = 100  # -99 DIE IN SINGLE CONTACT
        self.hp = self.hpmax
        self.engine = 0.3
        self.loss = 0.04
        self.engine_max = 4
        self.active_bonuses = {}
        self.myshield = None
        self.mass = 95
        self.direction = 90
        selfRADdirection = 0.5 * pi
        self.bullet_maxspeed = 8
        self.bouncesWith = ['Asteroid']

        cX, cY, R = self.x, self.y, self.radius
        self.dots = {
            'midcenter': (floor(cX), floor(cY)),
            'left': (floor(cX - R), floor(cY)),
            'right': (floor(cX + R), floor(cY)),
            'top': (floor(cX), floor(cY - R)),
            'bottom': (floor(cX), floor(cY + R))
        }

    def event_aftermove(self):
        """
        Действия после перемещения
        :return: None
        """
        if self.x < 10:
            self.x = 10
        if self.x > LEVEL_WIDTH - 10:
            self.x = LEVEL_WIDTH - 10
        if self.y < 10:
            self.y = 10
        if self.y > LEVEL_HEIGHT - 20:
            self.y = LEVEL_HEIGHT - 20

        super().event_aftermove()

    def move(self):
        """
        Действия при перемещении
        :return: None
        """
        self.update_VD()
        super().move()

    def draw(self):
        """
        Отрисовка объекта
        :return: None
        """
        global window
        super().draw()
        x, y = self.drawpoz()

        # draw HP BAR
        pygame.draw.rect(window, (100, 100, 100), (self.x - 30, self.y + 35, 60, 10))
        pygame.draw.rect(window, (15, 255, 55), (self.x - 28, self.y + 37, round(58 * self.hp / self.hpmax), 8))
        # draw SPEED BAR
        pygame.draw.rect(window, (100, 100, 100), (self.x - 30, self.y + 45, 60, 10))
        pygame.draw.rect(window, (200, 100, 100),
                         (self.x - 28, self.y + 47, round(58 * abs(self.speed) / self.engine_max), 8))

        if 'invincible' in self.active_bonuses:
            time = self.active_bonuses['invincible']
            if time > 0:
                gonePrc = time / 500
                wid = round(1 + (gonePrc * 20))
                pygame.draw.circle(window, rgb(0, 255, 0), self.drawpoz(), self.radius + 4, wid)

        if 'hp_regen' in self.active_bonuses:
            if self.active_bonuses['hp_regen'] > 0:
                pygame.draw.circle(window, rgb(255, 30, 30), self.drawpoz(), 4, 3)

        write('#Z' + str(len(self.myZones)), (255, 255, 255), (x - 50, y))

    def event_create(self):
        """
        Создание объекта
        :return: None
        """
        super().event_create()
        self.hp = 50
        self.active_bonuses = {'hp_regen': 300, 'speed_bonus+5': 1000, 'invincible': 250, 'allNeweffects place here': 0}

    def event_destroy(self):
        """
        Действия при разрушении объекта
        :return: None
        """

        if self.myshield != None:
            DestroyUID(self.myshield)

        global NOTIFY
        global LIVES
        if LIVES > 0:
            LIVES -= 1

            def Reborn():
                AddNewObj(Player(512, 650))

            AddNewObj(Timer(200, 200, Reborn, 1))

            NOTIFY = 'Reborn! Lives: ' + str(LIVES)
        else:
            NOTIFY = 'Game Over...   Score:' + str(STATISTICS['score']) + '            PRESS R to restart'

    def event_step(self):
        """
        Метод вызывающейся каждый игровой такт
        после перемещения но перед обработкой столкновений
        для обработки специфической персональной логики
        объекта.
        :return: None
        """

        # friction
        sign = -1 if self.speed < 0 else 1

        if abs(self.speed) > 0:
            self.speed -= self.loss * sign
        else:
            self.speed = 0

        # IF ALIVE  or not?
        if self.hp < 0:
            print('Your have been exploded')
            DestroyObj(self)

        # SELF REPAIR (BASIC REGENERATION)
        if self.hp < self.hpmax:
            self.hp += 0.05

        # BONUSES
        for bonus in self.active_bonuses:
            if self.active_bonuses[bonus] > 0:

                self.active_bonuses[bonus] -= 1
                if self.active_bonuses[bonus] < 0:
                    print(bonus, ' effect has expired')

                if bonus == 'hp_regen':
                    if self.hp < self.hpmax:
                        self.hp += 0.3

    def ev_react(self, the_event):
        """
        Реакция на нажатие клавиш
        :param the_event: клавиша
        :return: None
        """

        global pressed
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            self.speed = min(self.engine_max, self.speed + self.engine)
        if pressed[pygame.K_s]:
            self.speed = max(-1 * self.engine_max, self.speed - self.engine)

        if pressed[pygame.K_a]:
            self.update_directionDEG(3)
        if pressed[pygame.K_d]:
            self.update_directionDEG(-3)

        if not pressed[pygame.K_a] and not pressed[pygame.K_d]:
            self.xspeed = 0
        if not pressed[pygame.K_w] and not pressed[pygame.K_s]:
            self.yspeed = 0

        if True:

            if the_event.type == pygame.MOUSEBUTTONDOWN:
                # print(the_event.button)
                if the_event.button == 1:
                    self.bullet_maxspeed = 8

                    V = RadAngleToVec(self.RADdirection) * self.bullet_maxspeed

                    _xspeed, _yspeed = V

                    AddNewObj(Bullet(self.x, self.y - 15, _xspeed, _yspeed))
                    inc('bulletsAll')

                if the_event.button == 2:
                    i = self
                    xx, yy = pygame.mouse.get_pos()
                    xdif, ydif = xx - i.x, yy - i.y
                    most = max(abs(xdif), abs(ydif), 1)
                    xdose, ydose = xdif / most, ydif / most
                    _maxspeed = 6
                    _xspeed, _yspeed = _maxspeed * xdose, _maxspeed * ydose

                    AddNewObj(Bouncer(self.x, self.y - 15, _xspeed, _yspeed, S_get('heavy')))
                    inc('bulletsAll')

                if the_event.button == 3:

                    if self.myshield == None or (self.myshield not in allObjects):
                        AddNewObj(Shield(self))

            if the_event.type == pygame.MOUSEBUTTONUP:

                if the_event.button == 3:

                    if self.myshield != None:
                        DestroyUID(self.myshield)

            if the_event.type == pygame.KEYDOWN:

                if the_event.key == pygame.K_a:
                    self.update_directionDEG(5)

                if the_event.key == pygame.K_d:
                    self.update_directionDEG(-5)

                if the_event.key == pygame.K_RETURN:
                    AddNewObj(Asteroid(512, 426))

                if the_event.key == pygame.K_KP_ENTER:
                    AddNewObj(Bullet(self.x, self.y - 15))


allObjects = {}
constructors = []
destructors = set()

uid = 100000

from quad_collider import RegionNode as Node

Leaves = set()  # this is set of unique values that are store each of them only in one and only one exmplaire
Root = Node([0, 0, LEVEL_WIDTH, LEVEL_HEIGHT], None, 'R', [], Leaves)


def SolveTheCollidement(objA, objB, a_reacts, b_reacts, dist, rrsum):
    """
    Функция разрешающая столновения двух объектов
    :param objA: первый объект
    :param objB: второй объект
    :param a_reacts: реакция первого на второго
    :param b_reacts: реакция второго на первого
    :param dist: дистанция между объектами
    :param rrsum: сумма радиусов
    :return: None
    """
    inc('Bounces')
    A, B = objA, objB

    dx = B.x - A.x
    dy = B.y - A.y
    N = _V2(dx, dy)

    if N == (0, 0):
        uN = N
    else:
        uN = N.normalize()

    uT = _V2(- uN.y, uN.x)

    ax, ay = A.xprev, A.yprev
    bx, by = B.xprev, B.yprev
    prevdist = distanceBetweenPoints(ax, ay, bx, by)
    diffdist = dist - prevdist

    achieved = False
    dose = 0.90
    while dose >= 0:
        ax, ay = A.xprev + A.xspeed * dose, A.yprev + A.yspeed * dose
        bx, by = B.xprev + B.yspeed * dose, B.yprev + B.yspeed * dose
        optidist = distanceBetweenPoints(ax, ay, bx, by)
        if optidist > rrsum:
            achieved = True
            break
        dose -= 0.10
    A.x, A.y = ax, ay
    B.x, B.y = bx, by
    if not achieved:
        if A._is('Asteroid') and B._is('Asteroid'):
            A.prevBounces[B.uid] = 1 if B.uid not in A.prevBounces else 1 + A.prevBounces[B.uid]
            B.prevBounces[A.uid] = 1 if A.uid not in A.prevBounces else 1 + A.prevBounces[A.uid]

        ax, ay = A.xprev, A.yprev
        bx, by = B.xprev, B.yprev
        dose = 0

    V1 = _V2(A.xspeed, A.yspeed)
    V2 = _V2(B.xspeed, B.yspeed)

    V1n = uN.dot(V1)
    V1t = uT.dot(V1)
    V2n = uN.dot(V2)
    V2t = uT.dot(V2)

    m1, m2 = A.mass, B.mass
    total_mass = m1 + m2

    V1t_ = V1t
    V2t_ = V2t
    V1n_ = (V1n * (m1 - m2) + 2 * m2 * V2n) / (m1 + m2)
    V2n_ = (V2n * (m2 - m1) + 2 * m1 * V1n) / (m1 + m2)

    newV1n = V1n_ * uN
    newV1t = V1t_ * uT
    newV2n = V2n_ * uN
    newV2t = V2t_ * uT

    newV1FINAL = newV1n + newV1t
    newV2FINAL = newV2n + newV2t

    if a_reacts:
        A.xspeed, A.yspeed = newV1FINAL
        A.prevBounces[B.uid] = 1 if B.uid not in A.prevBounces else 1 + A.prevBounces[B.uid]

    if b_reacts:
        B.xspeed, B.yspeed = newV2FINAL
        B.prevBounces[A.uid] = 1 if A.uid not in A.prevBounces else 1 + A.prevBounces[A.uid]

    dose = dose - 1.2
    A.x, A.y = ax + A.xspeed * dose, ay + A.yspeed * dose
    B.x, B.y = bx + B.yspeed * dose, by + B.yspeed * dose


LevelBrains = None
PrepareGameLevel()
Update()
DrawAll()

ResetTree()

DrawAll()

# override pre base initialization of variables
pause = False
wait = False
run = True
pressed = []
collided = False
allowCollide = True

prevpause = pause

while run:

    clock.tick(60)
    inc('step')
    happends = pygame.event.get()
    pressed = pygame.key.get_pressed()

    ReactEventsAll(happends, pressed)

    if not pause:
        Update()
        MoveAll()
        AfterMoveAll()
        StepAll()
        CollideAll()
        AfterStepAll()
    DrawAll()

Finalize()
