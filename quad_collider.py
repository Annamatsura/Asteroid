from geo_inter_sections import *

MAX_OBJECTS_INSIDE = 3
MAX_SIZE_REGION = 50

from math import floor, sqrt

Apoint = 'Apoint'
Zpoint = 'Zpoint'


class RegionNode:
    """
    Узел (элемент/нода) дерева.
        Каждая имеет или 0 или 4 дочерних ноды такого же типа (дочерние узлы, субветки)
    """

    def distAB_2(self, pointA, pointB):
        return (pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2

    def distAB(self, pointA, pointB):
        return sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)

    def __init__(self, points=[0, 0, 0, 0], parent=None, index='?', subzones=[], LeavesList=None, stepborn=-1):
        """
        Инициализация
        :param points: [Ax,Ay,  Bx,By]  - координаты  верхнего левого края и нижней правого края зоны даного узла
        :param parent: указатель на родительскую Ноду. обычно это или кореньRoot или личный родитель
        :param index: буква-идентификатор охватываемого веткой субрегиона(A,B, С или D)
        :param subzones: [] список субветок. или 4 или пусто
        :param LeavesList: cссылка на список хранящий в себе все переферийные листы.
        туда будем вписывать новые переферическе личты и удалять ветки переставшие быть переферицными
        :param stepborn:
        """

        # ставим дефолтные значения
        if points == None:
            points = [0, 0, 0, 0]
        self.stepborn = stepborn
        self.playerIn = (100, 100, 100)
        self.level = 0  # уровень вложенности (углбленности внутрь дерева. корень имеет 0, первые узлы 1, последующие 2, 3, 4, итд
        self.index = index
        self.fulladress = self.index  # полный адрес до ветки.например для глубины 7 адресс будет R->A->A->C->B->D->A
        if parent != None:
            self.level = parent.level + 1
            self.fulladress = parent.fulladress + self.index

        x1, y1, x2, y2 = points

        self.points = [(x1, y1), (x2, y2)]

        # region constarints
        self.leftX = min(x1, x2)
        self.rightX = max(x1, x2)

        self.bottomY = max(y1, y2)
        self.topY = min(y1, y2)
        self.dots = {
            'A': (self.leftX, self.topY),
            'B': (self.rightX, self.topY),
            'C': (self.rightX, self.bottomY),
            'D': (self.leftX, self.bottomY)
        }
        self.lines = {'AB': (self.dots['A'], self.dots['B']),
                      'BC': (self.dots['B'], self.dots['C']),
                      'CD': (self.dots['C'], self.dots['D']),
                      'DA': (self.dots['D'], self.dots['A']),
                      }

        self.rangeX = range(self.leftX, self.rightX)
        self.rangeY = range(self.topY, self.bottomY)
        self.width = self.rightX - self.leftX + 1
        self.height = self.bottomY - self.topY + 1

        self.subzones = subzones
        self.upperzone = None
        self.objects = set()
        self.overloaded = False
        self.parent = parent

        self.Leaves = LeavesList
        self.totalObj = 0

    def put(self, obj):
        """
        Вносит обьект в перечень этой зоны(ноды, узла, ветки)и если нужно то также в её родительские
        :param obj: объект
        :return: None
        """
        zone = self

        hizone = self
        while hizone != None:

            hizone.totalObj += 1
            hizone.objects.add(obj)
            obj.myZones.add(hizone)

            hizone = hizone.parent
            # only for UpdateTreeMode not for ResetTreeMode:
            if True: break

    def put_protected(self, obj):
        """
        Вносит обьект в перечень этой зоны(ноды, узла, ветки) но не в ее вышестоящих родителей
        :param obj: объект
        :return: None
        """
        if obj in self.objects:
            return
        else:
            self.put(obj)

    # ----------------GEOINSIDE CHECK==============
    def is_geoinside(self, obj, wantToPut=False):
        """
        проверяет находиться ли обьект obj внутри текущей зоны
        :param obj: объект
        :param wantToPut:
        :return:
        """
        zone = self

        # CHECK: wether any object point is inside of zone`s rectangle
        # for rigid multipointed directly  connected figures of 3,4,5,6,7 etc point with direct connect
        if obj.form in ['circle', 'triangle', 'rectangle', 'romb', 'paralelogram']:

            for dotObj in obj.dots.values():
                objDotX, objDotY = floor(dotObj[0]), floor(dotObj[1])

                if objDotX in zone.rangeX and objDotY in zone.rangeY:
                    if wantToPut:
                        self.put(obj)
                        if obj._is('Player'): zone.playerIn = (50, 255, 70)
                    return True

        # specifical for circles
        # CHECK: wether any zone point is  inside circle
        # when zonecorner inside circle.

        if obj.form in ['circle', 'ellipseNOtWorkingYet=)']:
            for sidepointZ in zone.dots.values():
                if self.distAB(obj._xy(), sidepointZ) < obj.radius:
                    if wantToPut:
                        self.put(obj)
                        if obj._is('Player'): zone.playerIn = (50, 50, 255)
                    return True

        # CHECK: wether any figure`s line intersects any of zone`s line
        # '''
        # specifical for rigid multipointed directly interconnected figures of 3,4,5,6,7 etc point with direct connect
        # line intersection check
        if obj.form == 'triangle':
            for oln, objLine in obj.lines.items():
                for zln, zoneline in zone.lines.items():
                    rez = line_x_line(objLine, zoneline)

                    if rez:
                        # if obj._is('Player'): print(oln,zln,rez,'of intersects for Player')
                        if wantToPut:
                            self.put(obj)
                            if obj._is('Player'): zone.playerIn = (255, 151, 151)
                        return True
        return False

    def inout(self, obj):
        """
        если обьект входит в геозону  то вписывает его в список,
        если не входит то вычеркивает
        :param obj: объект
        :return: None
        """
        if not self.is_geoinside(obj):
            self.leave(obj)
        else:
            self.put_protected(obj)

    def leave(self, obj):
        """
        если объект содержался в текущей зоне - вычеркнуть его
        :param obj: объект
        :return: None
        """
        if obj not in self.objects:  return

        self.objects.remove(obj)

        senior = self.parent
        while senior != None:
            senior.totalObj += 1
            senior = senior.parent

    def wether_geoleave(self, obj):
        """
        проверить покинул obj нашу геозону или нет
        если покинул то вычеркнуть
        :param obj: объект
        :return: None
        """
        if not self.is_geoinside(obj):
            self.leave(obj)

    def _info_(self):
        """
        выводит структурированый отчет о текущей ветке
        :return: None
        """
        me = self
        L, R, T, B, W, H = me.leftX, me.rightX, me.topY, me.bottomY, me.width, me.height

        objs = [str(obj.uid) + ' ' + obj._am() + ',' for obj in self.objects]
        print('id:', id(self), ' age:', self.stepborn, ' lvl:', self.level, ')', ' ' * 5 * self.level, self.index,
              ' at (', self.fulladress, ') , ', ' has objects:', len(self.objects), 'pcs:', objs, sep='')
        # ,W,'x',H,';  ',self.rangeX,',', self.rangeY, ',

    def investigate(self):
        """
        выводит в консоль рекурсивное описание всего дерева
        :return:
        """
        if True or len(self.objects) > 0:
            self._info_()

        for subzone in self.subzones:
            subzone.investigate()

    def freeAll(self):
        """
        выводит в консоль рекурсивное описание всего дерева
        :return:
        """
        for subzone in self.subzones:
            subzone.freeAll()

        del self

    def divide(self):
        """
        разбивает ноду на 4 субноды и делит свои обьекты между ними 4мя
        предотвращает бесконечно мелкое дробление на минимальном оправданном размере 30-50 пикселей около
        используется при переполнении ноды обьектами
        :return: None
        """
        if self.width < MAX_SIZE_REGION and self.height < MAX_SIZE_REGION:
            return

        self.playerIn = (100, 100, 100)
        self.Leaves.remove(self)
        papa = self
        me = self

        # calculate borders
        L, R, T, B, W, H = me.leftX, me.rightX, me.topY, me.bottomY, me.width, me.height
        midX, midY = floor(L + W / 2), floor(T + H / 2)

        borders = {
            'A': [L, T, midX - 1, midY - 1],
            'B': [midX - 1, T, R, midY - 1],
            'C': [midX, midY, R, B],
            'D': [L, midY, midX, B]

        }

        # породить четверку наследников
        A, B, C, D = [RegionNode(border, papa, letter, [], self.Leaves, self.stepborn) for letter, border in
                      borders.items()]

        papa.subzones = [A, B, C, D]
        for elm in papa.subzones:
            self.Leaves.add(elm)

        #  раздать наследие среди четверки 
        for zone in [A, B, C, D]:

            for obj in self.objects:
                zone.is_geoinside(obj, wantToPut=True)

        # Деление субзон до конца
        for zone in [A, B, C, D]:
            size = len(zone.objects)
            if size > MAX_OBJECTS_INSIDE:
                zone.overloaded = False
                zone.playerIn = (100, 100, 100)
                zone.divide()

        # UPDATE TREE MODE ONLY self.objects = self.objects
        # if usual mode:
        self.objects = []
