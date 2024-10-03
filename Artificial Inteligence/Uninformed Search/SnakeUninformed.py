import bisect

"""
Дефинирање на класа за структурата на проблемот кој ќе го решаваме со пребарување.
Класата Problem е апстрактна класа од која правиме наследување за дефинирање на основните 
карактеристики на секој проблем што сакаме да го решиме
"""


class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """За дадена состојба, врати речник од парови {акција : состојба}
        достапни од оваа состојба. Ако има многу следбеници, употребете
        итератор кој би ги генерирал следбениците еден по еден, наместо да
        ги генерирате сите одеднаш.
        :param state: дадена состојба
        :return:  речник од парови {акција : состојба} достапни од оваа
                  состојба
        :rtype: dict
        """
        raise NotImplementedError

    def actions(self, state):
        """За дадена состојба state, врати листа од сите акции што може да
        се применат над таа состојба
        :param state: дадена состојба
        :return: листа на акции
        :rtype: list
        """
        raise NotImplementedError

    def result(self, state, action):
        """За дадена состојба state и акција action, врати ја состојбата
        што се добива со примена на акцијата над состојбата
        :param state: дадена состојба
        :param action: дадена акција
        :return: резултантна состојба
        """
        raise NotImplementedError

    def goal_test(self, state):
        """Врати True ако state е целна состојба. Даденава имплементација
        на методот директно ја споредува state со self.goal, како што е
        специфицирана во конструкторот. Имплементирајте го овој метод ако
        проверката со една целна состојба self.goal не е доволна.
        :param state: дадена состојба
        :return: дали дадената состојба е целна состојба
        :rtype: bool
        """
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Врати ја цената на решавачкиот пат кој пристигнува во состојбата
        state2 од состојбата state1 преку акцијата action, претпоставувајќи
        дека цената на патот до состојбата state1 е c. Ако проблемот е таков
        што патот не е важен, оваа функција ќе ја разгледува само состојбата
        state2. Ако патот е важен, ќе ја разгледува цената c и можеби и
        state1 и action. Даденава имплементација му доделува цена 1 на секој
        чекор од патот.
        :param c: цена на патот до состојбата state1
        :param state1: дадена моментална состојба
        :param action: акција која треба да се изврши
        :param state2: состојба во која треба да се стигне
        :return: цена на патот по извршување на акцијата
        :rtype: float
        """
        return c + 1

    def value(self):
        """За проблеми на оптимизација, секоја состојба си има вредност.
        Hill-climbing и сличните алгоритми се обидуваат да ја максимизираат
        оваа вредност.
        :return: вредност на состојба
        :rtype: float
        """
        raise NotImplementedError


"""
Дефинирање на класата за структурата на јазел од пребарување.
Класата Node не се наследува
"""


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Креирај јазол од пребарувачкото дрво, добиен од parent со примена
        на акцијата action
        :param state: моментална состојба (current state)
        :param parent: родителска состојба (parent state)
        :param action: акција (action)
        :param path_cost: цена на патот (path cost)
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0  # search depth
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """Излистај ги јазлите достапни во еден чекор од овој јазол.
        :param problem: даден проблем
        :return: листа на достапни јазли во еден чекор
        :rtype: list(Node)
        """
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """Дете јазел
        :param problem: даден проблем
        :param action: дадена акција
        :return: достапен јазел според дадената акција
        :rtype: Node
        """
        next_state = problem.result(self.state, action)
        return Node(next_state, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_state))

    def solution(self):
        """Врати ја секвенцата од акции за да се стигне од коренот до овој јазол.
        :return: секвенцата од акции
        :rtype: list
        """
        return [node.action for node in self.path()[1:]]

    def solve(self):
        """Врати ја секвенцата од состојби за да се стигне од коренот до овој јазол.
        :return: листа од состојби
        :rtype: list
        """
        return [node.state for node in self.path()[0:]]

    def path(self):
        """Врати ја листата од јазли што го формираат патот од коренот до овој јазол.
        :return: листа од јазли од патот
        :rtype: list(Node)
        """
        x, result = self, []
        while x:
            result.append(x)
            x = x.parent
        result.reverse()
        return result

    """Сакаме редицата од јазли кај breadth_first_search или 
    astar_search да не содржи состојби - дупликати, па јазлите што
    содржат иста состојба ги третираме како исти. [Проблем: ова може
    да не биде пожелно во други ситуации.]"""

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


"""
Дефинирање на помошни структури за чување на листата на генерирани, но непроверени јазли
"""


class Queue:
    """Queue е апстрактна класа / интерфејс. Постојат 3 типа:
        Stack(): Last In First Out Queue (стек).
        FIFOQueue(): First In First Out Queue (редица).
        PriorityQueue(order, f): Queue во сортиран редослед (подразбирливо,од најмалиот кон
                                 најголемиот јазол).
    """

    def __init__(self):
        raise NotImplementedError

    def append(self, item):
        """Додади го елементот item во редицата
        :param item: даден елемент
        :return: None
        """
        raise NotImplementedError

    def extend(self, items):
        """Додади ги елементите items во редицата
        :param items: дадени елементи
        :return: None
        """
        raise NotImplementedError

    def pop(self):
        """Врати го првиот елемент од редицата
        :return: прв елемент
        """
        raise NotImplementedError

    def __len__(self):
        """Врати го бројот на елементи во редицата
        :return: број на елементи во редицата
        :rtype: int
        """
        raise NotImplementedError

    def __contains__(self, item):
        """Проверка дали редицата го содржи елементот item
        :param item: даден елемент
        :return: дали queue го содржи item
        :rtype: bool
        """
        raise NotImplementedError


class Stack(Queue):
    """Last-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop()

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class FIFOQueue(Queue):
    """First-In-First-Out Queue."""

    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def extend(self, items):
        self.data.extend(items)

    def pop(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data


class PriorityQueue(Queue):
    """Редица во која прво се враќа минималниот (или максималниот) елемент
    (како што е определено со f и order). Оваа структура се користи кај
    информирано пребарување"""
    """"""

    def __init__(self, order=min, f=lambda x: x):
        """
        :param order: функција за подредување, ако order е min, се враќа елементот
                      со минимална f(x); ако order е max, тогаш се враќа елементот
                      со максимална f(x).
        :param f: функција f(x)
        """
        assert order in [min, max]
        self.data = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort_right(self.data, (self.f(item), item))

    def extend(self, items):
        for item in items:
            bisect.insort_right(self.data, (self.f(item), item))

    def pop(self):
        if self.order == min:
            return self.data.pop(0)[1]
        return self.data.pop()[1]

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.data)

    def __getitem__(self, key):
        for _, item in self.data:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.data):
            if item == key:
                self.data.pop(i)


import sys

"""
Неинформирано пребарување во рамки на дрво.
Во рамки на дрвото не разрешуваме јамки.
"""


def tree_search(problem, fringe):
    """ Пребарувај низ следбениците на даден проблем за да најдеш цел.
    :param problem: даден проблем
    :type problem: Problem
    :param fringe:  празна редица (queue)
    :type fringe: FIFOQueue or Stack or PriorityQueue
    :return: Node or None
    :rtype: Node
    """
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        print(node.state)
        if problem.goal_test(node.state):
            return node
        fringe.extend(node.expand(problem))
    return None


def breadth_first_tree_search(problem):
    """Експандирај го прво најплиткиот јазол во пребарувачкото дрво.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    return tree_search(problem, FIFOQueue())


def depth_first_tree_search(problem):
    """Експандирај го прво најдлабокиот јазол во пребарувачкото дрво.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    return tree_search(problem, Stack())


"""
Неинформирано пребарување во рамки на граф
Основната разлика е во тоа што овде не дозволуваме јамки, 
т.е. повторување на состојби
"""


def graph_search(problem, fringe):
    """Пребарувај низ следбениците на даден проблем за да најдеш цел.
     Ако до дадена состојба стигнат два пата, употреби го најдобриот пат.
    :param problem: даден проблем
    :type problem: Problem
    :param fringe:  празна редица (queue)
    :type fringe: FIFOQueue or Stack or PriorityQueue
    :return: Node or None
    :rtype: Node
    """
    closed = set()
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        if node.state not in closed:
            closed.add(node.state)
            fringe.extend(node.expand(problem))
    return None


def breadth_first_graph_search(problem):
    """Експандирај го прво најплиткиот јазол во пребарувачкиот граф.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    return graph_search(problem, FIFOQueue())


def depth_first_graph_search(problem):
    """Експандирај го прво најдлабокиот јазол во пребарувачкиот граф.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    return graph_search(problem, Stack())


def depth_limited_search(problem, limit=50):
    """Експандирај го прво најдлабокиот јазол во пребарувачкиот граф
    со ограничена длабочина.
    :param problem: даден проблем
    :type problem: Problem
    :param limit: лимит за длабочината
    :type limit: int
    :return: Node or None
    :rtype: Node
    """

    def recursive_dls(node, problem, limit):
        """Помошна функција за depth limited"""
        cutoff_occurred = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
        if cutoff_occurred:
            return 'cutoff'
        return None

    return recursive_dls(Node(problem.initial), problem, limit)


def iterative_deepening_search(problem):
    """Експандирај го прво најдлабокиот јазол во пребарувачкиот граф
    со ограничена длабочина, со итеративно зголемување на длабочината.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result


def uniform_cost_search(problem):
    """Експандирај го прво јазолот со најниска цена во пребарувачкиот граф.
    :param problem: даден проблем
    :type problem: Problem
    :return: Node or None
    :rtype: Node
    """
    return graph_search(problem, PriorityQueue(min, lambda a: a.path_cost))


def ProdolzhiPravo(snakeH, snakeB, zeleni, nasoka, crveni):
    l = len(snakeB)
    temporary = snakeB[-1]  # poslednoto delce go stavame u temporary promenliva. zosto.
    # za da vidime ako treba da se zgoleme zmijata treba da se dodade taa torka podole.
    snakeB = list(snakeB)
    att = [snakeB[-1]] + snakeB[:-1]  # pridvizuvanje na teloto na zmijata,
    # se prebrisuva prviot element najblisku do glavata so toa so
    snakeH = list(snakeH)
    att[
        0] = snakeH  # se izminuva celoto telo i se zamenuvat vrednostite za delceto pozadi vo redicata so e so pred nego
    att[0] = tuple(att[0])
    snakeB[-1] = tuple(snakeB[-1])
    # prviot del od teloto so e najblisku do glavata treba da bide sega kaj so bila glavata, glavata uste ne e promeneta
    snakeB = tuple(att)
    snakeH = tuple(snakeH)
    new_apples = zeleni
    if nasoka == "jug":  # samo y koordinata treba da smenime, ostanuva na istata x
        if int(snakeH[1]) - 1 >= 0 and (snakeH[0], int(snakeH[1]) - 1) not in crveni and (
        snakeH[0], int(snakeH[1]) - 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) - 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) - 1)]
            return (int(snakeH[0]), int(snakeH[1]) - 1), snakeB, tuple(
                new_apples), nasoka, crveni  # glavata da a pridvizime za 1
    if nasoka == "sever":
        if int(snakeH[1]) + 1 <= 9 and int(snakeH[1]) + 1 >= 0 and (snakeH[0], int(snakeH[1]) + 1) not in crveni and (
        snakeH[0], int(snakeH[1]) + 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) + 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) + 1)]
            return (int(snakeH[0]), int(snakeH[1]) + 1), snakeB, tuple(
                new_apples), nasoka, crveni  # glavata da a pridvizime za 1
    if nasoka == "istok":
        if int(snakeH[0]) + 1 <= 9 and int(snakeH[0]) + 1 >= 0 and (int(snakeH[0]) + 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) + 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) + 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) + 1, snakeH[1])]
            return (int(snakeH[0]) + 1, int(snakeH[1])), snakeB, tuple(new_apples), nasoka, crveni
    if nasoka == "zapad":
        if int(snakeH[0]) - 1 >= 0 and (int(snakeH[0]) - 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) - 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) - 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) - 1, snakeH[1])]
            return (int(snakeH[0]) - 1, int(snakeH[1])), snakeB, tuple(new_apples), nasoka, crveni
    return (-1, -1), (-1, -1), (-1, -1), (-1, -1), "error"


def SvrtiDesno(snakeH, snakeB, zeleni, nasoka, crveni):
    l = len(snakeB)
    temporary = snakeB[-1]  # poslednoto delce go stavame u temporary promenliva. zosto.
    # za da vidime ako treba da se zgoleme zmijata treba da se dodade taa torka podole.
    snakeB = list(snakeB)
    att = [snakeB[-1]] + snakeB[:-1]  # pridvizuvanje na teloto na zmijata,
    # se prebrisuva prviot element najblisku do glavata so toa so
    snakeH = list(snakeH)
    att[
        0] = snakeH  # se izminuva celoto telo i se zamenuvat vrednostite za delceto pozadi vo redicata so e so pred nego
    att[0] = tuple(att[0])
    snakeB[-1] = tuple(snakeB[-1])
    # prviot del od teloto so e najblisku do glavata treba da bide sega kaj so bila glavata, glavata uste ne e promeneta
    snakeB = tuple(att)
    snakeH = tuple(snakeH)
    new_apples = zeleni
    if nasoka == "sever":  # ode od ^ na ->, x koordinata se menuva od n na n+1
        if int(snakeH[0]) + 1 <= 9 and (int(snakeH[0]) + 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) + 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) + 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) + 1, snakeH[1])]
            return ((int(snakeH[0])) + 1, int(snakeH[1])), snakeB, tuple(new_apples), "istok", crveni
    if nasoka == "jug":  # ode od v na <-, x koordinata se menuva od n na n-1
        if int(snakeH[0]) - 1 >= 0 and (int(snakeH[0]) - 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) - 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) - 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) - 1, snakeH[1])]
            return ((int(snakeH[0])) - 1, int(snakeH[1])), snakeB, tuple(new_apples), "zapad", crveni
    if nasoka == "istok":  # ode od -> na v, y koordinata se menuva od n na n-1
        if int(snakeH[1]) - 1 >= 0 and (snakeH[0], int(snakeH[1]) - 1) not in crveni and (
        snakeH[0], int(snakeH[1]) - 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) - 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) - 1)]
            return (int(snakeH[0]), int(snakeH[1]) - 1), snakeB, tuple(new_apples), "jug", crveni
    if nasoka == "zapad":  # ode od <- na ^, y koordinata se menuva od n na n+1
        if int(snakeH[1]) + 1 <= 9 and (snakeH[0], int(snakeH[1]) + 1) not in crveni and (
        snakeH[0], int(snakeH[1]) + 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) + 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) + 1)]
            return (int(snakeH[0]), int(snakeH[1]) + 1), snakeB, tuple(new_apples), "sever", crveni
    return (-1, -1), (-1, -1), (-1, -1), (-1, -1), "error"


def SvrtiLevo(snakeH, snakeB, zeleni, nasoka, crveni):
    l = len(snakeB)
    temporary = snakeB[-1]  # poslednoto delce go stavame u temporary promenliva. zosto.
    # za da vidime ako treba da se zgoleme zmijata treba da se dodade taa torka podole.
    snakeB = list(snakeB)
    att = [snakeB[-1]] + snakeB[:-1]  # pridvizuvanje na teloto na zmijata,
    # se prebrisuva prviot element najblisku do glavata so toa so
    snakeH = list(snakeH)
    att[
        0] = snakeH  # se izminuva celoto telo i se zamenuvat vrednostite za delceto pozadi vo redicata so e so pred nego
    att[0] = tuple(att[0])
    snakeB[-1] = tuple(snakeB[-1])
    # prviot del od teloto so e najblisku do glavata treba da bide sega kaj so bila glavata, glavata uste ne e promeneta
    snakeB = tuple(att)
    snakeH = tuple(snakeH)
    new_apples = zeleni
    if nasoka == "jug":  # ode od v na ->, x koordinata se menuva od n na n+1,
        if int(snakeH[0]) + 1 <= 9 and (int(snakeH[0]) + 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) + 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) + 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) + 1, snakeH[1])]
            return ((int(snakeH[0])) + 1, int(snakeH[1])), snakeB, tuple(new_apples), "istok", crveni
    if nasoka == "sever":  # ode od ^ na <-, x koordinata se menuva od n na n-1
        if int(snakeH[0]) - 1 >= 0 and (int(snakeH[0]) - 1, snakeH[1]) not in crveni and (
        int(snakeH[0]) - 1, snakeH[1]) not in snakeB:
            if (int(snakeH[0]) - 1, snakeH[1]) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (int(snakeH[0]) - 1, snakeH[1])]
            return ((int(snakeH[0])) - 1, int(snakeH[1])), snakeB, tuple(new_apples), "zapad", crveni
    if nasoka == "istok":  # ode od -> na ^, y koordinata se menuva od n na n+1
        if int(snakeH[1]) + 1 <= 9 and (snakeH[0], int(snakeH[1]) + 1) not in crveni and (
        snakeH[0], int(snakeH[1]) + 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) + 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) + 1)]
            return (int(snakeH[0]), int(snakeH[1]) + 1), snakeB, tuple(new_apples), "sever", crveni
    if nasoka == "zapad":  # ode od <- na v, y koordinata se menuva od n na n-1
        if int(snakeH[1]) - 1 >= 0 and (snakeH[0], int(snakeH[1]) - 1) not in crveni and (
        snakeH[0], int(snakeH[1]) - 1) not in snakeB:
            if (snakeH[0], int(snakeH[1]) - 1) in zeleni:
                snakeB = list(snakeB)
                snakeB.append(temporary)
                snakeB = tuple(snakeB)
                new_apples = [apple for apple in zeleni if apple != (snakeH[0], int(snakeH[1]) - 1)]
            return (int(snakeH[0]), int(snakeH[1]) - 1), snakeB, tuple(new_apples), "jug", crveni
    return (-1, -1), (-1, -1), (-1, -1), (-1, -1), "error"


class Snake(Problem):
    def __init__(self, initial, crveni_jabolki, goal=None):
        super().__init__(initial, goal)
        self.crveni_jabolki = crveni_jabolki  # oti ne se menjavat u tekot na prebaruvanjata
        # mozat da bidat u klasata deklarirani nezavisno od successors funkcijata

    def successor(self, state):
        successors = dict()
        snakeHead = state[0]  # samo edna torka na vrednosti
        snakeBody = state[1]  # lista od torki
        zeleni_jabolki = state[2]  # lista od torki za green apples
        nasoka = state[3]

        novo = ProdolzhiPravo(snakeHead, snakeBody, zeleni_jabolki, nasoka, crveni_jabolki)
        if novo[0][0] != -1 and novo[0][1] != -1:  # snake head x koord ne e -1 i snake head y koord ne e -1
            successors['ProdolzhiPravo'] = (novo[0], novo[1], novo[2], novo[3], novo[4])
        novo = SvrtiDesno(snakeHead, snakeBody, zeleni_jabolki, nasoka, crveni_jabolki)
        if novo[0][0] != -1 and novo[0][1] != -1:  # snake head x koord ne e -1 i snake head y koord ne e -1
            successors['SvrtiDesno'] = (novo[0], novo[1], novo[2], novo[3], novo[4])
        novo = SvrtiLevo(snakeHead, snakeBody, zeleni_jabolki, nasoka, crveni_jabolki)
        if novo[0][0] != -1 and novo[0][1] != -1:  # snake head x koord ne e -1 i snake head y koord ne e -1
            successors['SvrtiLevo'] = (novo[0], novo[1], novo[2], novo[3], novo[4])

        return successors

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return len(state[2]) == 0


if __name__ == "__main__":
    nGreen = int(input())  # number of green apples
    zeleni_jabolki = list()
    for i in range(0, nGreen):  # torkite na green apples da gi zeme
        el = input()  # od input
        brojcinja = el.split(",")
        add = int(brojcinja[0]), int(brojcinja[1])
        zeleni_jabolki.append(add)
    zeleni_jabolki = tuple(zeleni_jabolki)

    nRed = int(input())  # number of red apples
    crveni_jabolki = list()
    for i in range(0, nRed):
        el = input()  # od input
        brojcinja = el.split(",")
        add = int(brojcinja[0]), int(brojcinja[1])
        crveni_jabolki.append(add)
    crveni_jabolki = tuple(crveni_jabolki)

    snakeHead = (0, 7)
    snakeBody = ((0, 8), (0, 9))
    nasoka = "jug"
    snake = snakeHead, (snakeBody)
    zmija = Snake((snakeHead, snakeBody, zeleni_jabolki, nasoka), crveni_jabolki)
    result = breadth_first_graph_search(zmija)
    print(result.solution())