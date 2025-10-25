import sys
import heapq

ENERGY = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_POS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
VALID_HALL_POS = [0, 1, 3, 5, 7, 9, 10]


def parse_input(lines):
    rooms = []
    for i in range(4):
        col = 3 + 2 * i
        room = []
        for line in lines[2:-1]:
            if col < len(line) and line[col] in "ABCD":
                room.append(line[col])
        rooms.append(tuple(room))
    hallway = tuple("." for _ in range(11))
    return (hallway, tuple(rooms))


def is_finished(state):
    _, rooms = state
    for i, r in enumerate("ABCD"):
        if any(x != r for x in rooms[i]):
            return False
    return True


def moves_from_room_to_hallway(state, room_depth):
    hallway, rooms = state
    for i, room in enumerate(rooms):
        room_x = ROOM_POS["ABCD"[i]]
        if all(c == "ABCD"[i] for c in room if c != "."):
            continue  # Значит уже правильно
        # Находим верхнего амфипода
        for depth, c in enumerate(room):
            if c != ".":
                amphipod = c
                break
        else:
            continue
        # Путь вверх должен быть свободен
        steps_up = depth + 1
        # Проверяем все возможные позиции влево и вправо
        for dir in (-1, 1):
            x = room_x
            dist = steps_up
            while 0 <= x + dir < len(hallway):
                x += dir
                dist += 1
                if hallway[x] != ".":
                    break
                if x not in ROOM_POS.values():  # Можно стоять
                    new_hall = list(hallway)
                    new_hall[x] = amphipod
                    new_rooms = [list(r) for r in rooms]
                    new_rooms[i][depth] = "."
                    new_state = (tuple(new_hall), tuple(tuple(r) for r in new_rooms))
                    yield (
                        ENERGY[amphipod] * dist,
                        new_state,
                    )


def moves_from_hallway_to_room(state, room_depth):
    hallway, rooms = state
    for pos, c in enumerate(hallway):
        if c == ".":
            continue
        target_room_idx = "ABCD".index(c)
        room_x = ROOM_POS[c]
        room = rooms[target_room_idx]

        # Можно ли войти (в комнате только свой тип или пусто)
        if any(x != "." and x != c for x in room):
            continue
        # Проверяем, свободен ли путь
        step = 1 if room_x > pos else -1
        for x in range(pos + step, room_x + step, step):
            if hallway[x] != ".":
                break
        else:
            # Можно ли войти
            depth = room_depth - 1 - list(reversed(room)).index(".")
            dist = abs(room_x - pos) + depth + 1
            new_hall = list(hallway)
            new_hall[pos] = "."
            new_rooms = [list(r) for r in rooms]
            new_rooms[target_room_idx][depth] = c
            new_state = (tuple(new_hall), tuple(tuple(r) for r in new_rooms))
            yield (
                ENERGY[c] * dist,
                new_state,
            )


def dijkstra(start_state, room_depth):
    pq = [(0, start_state)]
    best = {start_state: 0}

    while pq:
        cost, state = heapq.heappop(pq)
        if cost != best[state]:
            continue
        if is_finished(state):
            return cost

        for move_func in (moves_from_hallway_to_room, moves_from_room_to_hallway):
            for add_cost, new_state in move_func(state, room_depth):
                new_cost = cost + add_cost
                if new_cost < best.get(new_state, 10 ** 12):
                    best[new_state] = new_cost
                    heapq.heappush(pq, (new_cost, new_state))
    return None


def solve(lines: list[str]) -> int:
    """
    Решение задачи о сортировке в лабиринте

    Args:
        lines: список строк, представляющих лабиринт

    Returns:
        минимальная энергия для достижения целевой конфигурации
    """

    # TODO: Реализация алгоритма
    start = parse_input(lines)
    room_depth = len(start[1][0])
    return dijkstra(start, room_depth)


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":

    main()
