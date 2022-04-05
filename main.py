from collections import defaultdict
from copy import copy
from itertools import zip_longest
from pprint import pprint

import numpy as np
from scipy.linalg import expm


def generate_states_set(customs, system):
    global L, H, states, temp

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
            generate_states_set(customs - temp[system], system + 1)


def get_achievable_states(state):
    global L, H, states, limits, mu, Theta

    achievable_states_and_rate = defaultdict(float)
    for l in range(L):
        if state[l] >= limits[l][0]:
            for g in range(limits[l][0], min(limits[l][1], state[l]) + 1):
                for sys in range(L):
                    gen_state = list(copy(state))
                    if sys != l:
                        gen_state[l] -= g
                        gen_state[sys] += g
                        gen_state = tuple(gen_state)
                        if gen_state in states:
                            achievable_states_and_rate[gen_state] = mu[l] * Theta[l][sys]

    return achievable_states_and_rate


def get_generator(_states):
    global mu, Theta

    n = len(_states)
    gen = np.zeros((n, n))
    for i, current_state in enumerate(_states):
        states_and_rates = get_achievable_states(current_state)
        for state, rate in states_and_rates.items():
            j = _states.index(state)
            gen[i, j] += rate

    for i, row in enumerate(gen):
        gen[i, i] = -sum(row)

    return gen

def mean_customs_num(L, H):
    s = [0] * L
    for i in range(L):
        for k in range(0, H + 1):
            summa_pi_for_k = 0
            for state_with_pi in states_to_pi:
                if state_with_pi[0][i] == k:
                    summa_pi_for_k += state_with_pi[1]

            s[i] += (k * summa_pi_for_k)
    return s


def flow_rate(L, limits, mu, states_to_pi):
    lambda_ = [0] * L
    for i in range(L):
        sum_k = 0
        for k in range(limits[i][0], limits[i][1] + 1):
            sum_pi = 0
            for state in states_to_pi:
                index = states_to_pi.index(state)
                for s in range(k):
                    if states_to_pi[index][0][i] == s:
                        sum_pi += states_to_pi[index][1]
            diff = 1 - sum_pi
            sum_k = sum_k + (k * diff)
        lambda_[i] = mu[i] * sum_k
    return lambda_


def response_time(L, s, lambda_):
    u = [0] * L
    for i in range(L):
        u[i] = s[i] / lambda_[i]
    return u


def waiting_in_queue(L, u, mu):
    w = [0] * L
    for i in range(L):
        w[i] = u[i] - (1 / mu[i])
    return w


def mean_customs_in_queue(L, lambda_, w):
    b = [0] * L
    for i in range(L):
        b[i] = lambda_[i] * w[i]
    return b


if __name__ == '__main__':
    L = 6
    H = 11
    limits = [(2, 7), (2, 5), (4, 6), (2, 6), (3, 7), (2, 4)]

    mu = [0.5, 1., 0.7, 0.4, 0.7, 0.5]
    Theta = np.array([
        [0., 0.21, 0.22, 0.18, 0.2, 0.19],
        [1., 0., 0., 0., 0., 0.],
        [1., 0., 0., 0., 0., 0.],
        [1., 0., 0., 0., 0., 0.],
        [1., 0., 0., 0., 0., 0.],
        [1., 0., 0., 0., 0., 0.]
    ])

    # L = 6
    # H = 10
    # limits = [(1, 3), (2, 3), (2, 4)]
    # mu = [0.5, 1., 0.7]
    # Theta = np.array([
    #     [0., 0.7, 0.3],
    #     [0.2, 0., 0.8],
    #     [0.5, 0.5, 0.]
    # ])

    states = list()
    temp = [0] * (L + 1)

    for i in range(H, 0, -1):
        generate_states_set(i, 1)

    print("states len list", len(states))
    generator = get_generator(states)

    print()

    np.savetxt("generator.txt", generator, fmt='%1.2f')
    pi = expm(generator * 100000000000)[0]
    pprint(pi)
    print(sum(pi))

    states_to_pi = list(zip_longest(states, pi))
    pprint(states_to_pi)

    s = mean_customs_num(L, H)
    print("М. о. числа требований в системах:", s, sum(s))

    lambda_ = flow_rate(L, limits, mu, states_to_pi)
    print("Интенсивность потока требований в системы:", lambda_)

    u = response_time(L, s, lambda_)
    print("М. о. длительности пребывания требований в системе:", u)

    w = waiting_in_queue(L, u, mu)
    print("М. о. длительности пребывания требований в очереди системы:", w)

    b = mean_customs_in_queue(L, lambda_, w)
    print("М. о. числа требований в очереди:", b)
