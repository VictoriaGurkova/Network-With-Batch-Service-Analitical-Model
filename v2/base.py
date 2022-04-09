def generate_states(L, H):
    states = list()
    temp = [0] * (L + 1)

    def _generate_states(customs, system):
        if system == L:
            state = []
            temp[system] = customs
            for m in range(1, L + 1):
                state.append(temp[m])
            if sum(state) == H:
                states.append(tuple(state))
        else:
            for k in range(customs, -1, -1):
                temp[system] = k
                _generate_states(customs - temp[system], system + 1)

    for i in range(H, 0, -1):
        _generate_states(i, 1)

    return states


def generate_Y():
    # todo: сгенерировать пространство векторов перемещений, состоящее из выходящих d и входящих a векторов
    pass


def generate_d():
    # todo: генерация выходящих векторов d, завясящих от ограничений (x_i, y_i)
    pass


def generate_a():
    # todo: генерация входящих векторов a (требований в системы обслуживания)
    pass
