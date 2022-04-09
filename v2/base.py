def generate_states(systems_number: int, all_customs: int) -> list:
    """
    Генерирует пространство состояний для заданных параметров закрытой сети

    :param systems_number: число систем в сети
    :param all_customs: число требований в закрытой сети
    :return: список (пространство) всех состояний сети
    """
    states = list()
    state_temp = [0] * (systems_number + 1)

    # system - номер рассматриваемой системы
    # customs - количество требований в системе
    def _generate_states(system: int, customs: int):
        if system == systems_number:
            state = []
            state_temp[system] = customs
            for m in range(1, systems_number + 1):
                state.append(state_temp[m])
            if sum(state) == all_customs:
                states.append(tuple(state))
        else:
            for k in range(customs, -1, -1):
                state_temp[system] = k
                _generate_states(system + 1, customs - state_temp[system])

    for i in range(all_customs, 0, -1):
        _generate_states(1, i)

    return states


# limits - ограничения на размер группы для каждой системы
def generate_Y(limits: list) -> set:
    d = generate_d(limits)
    a = generate_a(limits)
    return d.union(a)


def generate_d(limits: list) -> set:
    d = list()
    systems = len(limits)  # количество систем
    for index, limit in enumerate(limits):
        for customs in range(limit.x, limit.y + 1):
            d_temp = [0] * systems
            d_temp[index] = customs
            d.append(tuple(d_temp))
    return set(d)


def generate_a(limits: list) -> set:
    a = list()
    systems = len(limits)  # количество систем
    for index, limit in enumerate(limits):
        for customs in range(limit.x, limit.y + 1):
            for system in range(systems):
                if not system == index:
                    a_temp = [0] * systems
                    a_temp[system] = customs
                    a.append(tuple(a_temp))
    return set(a)
