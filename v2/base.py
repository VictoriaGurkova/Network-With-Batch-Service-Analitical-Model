from collections import defaultdict
from copy import copy

import numpy as np
from scipy.linalg import expm


def generate_states(systems_number: int, all_customs: int) -> list:
    """
    Генерирует пространство состояний для заданных параметров закрытой сети

    :param systems_number: число систем в сети
    :param all_customs: число требований в закрытой сети
    :return: список (пространство) всех состояний сети
    """
    states = list()
    state_temp = [0] * (systems_number + 1)

    def _generate_states(system: int, customs: int):
        """

        :param system: номер рассматриваемой системы
        :param customs: количество требований в системе
        :return:
        """
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


def get_achievable_states(state, states, limits, mu, Theta):
    achievable_states_and_rate = defaultdict(float)
    L = len(limits)  # количество систем

    for system_out in range(L):
        if state[system_out] >= limits[system_out].x:
            for group in range(limits[system_out].x, min(limits[system_out].y, state[system_out]) + 1):
                for system_in in range(L):
                    gen_state = list(copy(state))
                    if system_in != system_out:
                        gen_state[system_out] -= group
                        gen_state[system_in] += group
                        gen_state = tuple(gen_state)
                        if gen_state in states:
                            achievable_states_and_rate[gen_state] = mu[system_out] * Theta[system_out][system_in]

    return achievable_states_and_rate


def get_generator(states, limits, mu, Theta):
    n = len(states)
    generator = np.zeros((n, n))
    for i, current_state in enumerate(states):
        states_and_rates = get_achievable_states(current_state, states, limits, mu, Theta)
        for state, rate in states_and_rates.items():
            j = states.index(state)
            generator[i, j] += rate

    for i, row in enumerate(generator):
        generator[i, i] = -sum(row)

    return generator


def get_stationary_distribution(generator):
    pi = expm(generator * 1_000_000_000)[0]
    return pi


# limits - ограничения на размер группы для каждой системы
def generate_Y(limits: list) -> set:
    d = generate_d(limits)
    a = generate_a(limits)
    return d.union(a)


def generate_d(limits: list) -> set:
    d = list()
    L = len(limits)  # количество систем
    for index, limit in enumerate(limits):
        for customs in range(limit.x, limit.y + 1):
            d_temp = [0] * L
            d_temp[index] = customs
            d.append(tuple(d_temp))
    return set(d)


def generate_a(limits: list) -> set:
    a = list()
    L = len(limits)  # количество систем
    for index, limit in enumerate(limits):
        for customs in range(limit.x, limit.y + 1):
            for system in range(L):
                if not system == index:
                    a_temp = [0] * L
                    a_temp[system] = customs
                    a.append(tuple(a_temp))
    return set(a)


def get_omega(L, Theta):
    omega = np.array([1 / L for _ in range(L)])
    for _ in range(1_000_000):
        omega = omega.dot(Theta)
    return omega
