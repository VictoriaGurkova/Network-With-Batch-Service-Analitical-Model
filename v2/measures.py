from copy import copy
from math import factorial


def get_epsilon(omega, d, Y, r):
    L = len(omega)
    first, second = 1, 1
    
    for i in range(L):
        first *= (omega[i] ** d[i]) / factorial(d[i])

    Y_r = list(filter(lambda y: sum(y) == r, Y))
    summa = 0
    for d in Y_r:
        prod = 1
        for i in range(L):
            prod *= (omega[i] ** d[i]) / factorial(d[i])

        summa += prod
    second = 1 / summa

    epsilon = first * second

    # print("epsilon ->", epsilon)
    return epsilon


def get_P_r(states_to_pi, states, generator, Y, r):
    Y_r = list(filter(lambda y: sum(y) == r, Y))
    P_r = 0

    for d in Y_r:
        for pair in states_to_pi:
            P_r += (pair.pi * get_p_sd(generator, pair.state, d, states))

    # print("P_r ->", P_r)
    return P_r


def get_p_sd(generator, state, d, states):
    new_states = list()

    system_out = 0
    for index, element in enumerate(d):
        if element != 0:
            system_out = index

    for system_in in range(len(state)):
        gen_state = list(copy(state))
        if system_in != system_out:
            gen_state[system_out] -= d[system_out]
            gen_state[system_in] += d[system_out]
            gen_state = tuple(gen_state)
            if gen_state in states:
                new_states.append(gen_state)

    p_sd = 0
    state_index = states.index(state)
    for new_state in new_states:
        new_state_index = states.index(new_state)
        p_sd += generator[state_index, new_state_index]

    # print("p_sd ->", p_sd)
    return p_sd


def get_d_i(i, H, Y, states_to_pi, states, generator, omega):
    d_i = 0

    for r in range(H + 1):
        summa_2 = 0
        for m in range(r + 1):
            Y_r = list(filter(lambda y: sum(y) == r, Y))
            summa_1 = 0
            for d in Y_r:
                if d[i] == m:
                    summa_1 += get_epsilon(omega, d, Y, r)

            summa_2 += (m * summa_1)
        d_i += (get_P_r(states_to_pi, states, generator, Y, r) * summa_2)

    return d_i


def mean_customs_num(L, H, states_to_pi):
    s = [0] * L
    for i in range(L):
        for k in range(0, H + 1):
            summa_pi_for_k = 0
            for pair in states_to_pi:
                if pair.state[i] == k:
                    summa_pi_for_k += pair.pi

            s[i] += (k * summa_pi_for_k)
    return s


def response_time(L, s, d):
    u = [0] * L
    for i in range(L):
        u[i] = s[i] / d[i]
    return u


def waiting_in_queue(L, u, mu):
    w = [0] * L
    for i in range(L):
        w[i] = u[i] - (1 / mu[i])
    return w


def mean_customs_in_queue(L, d, w):
    b = [0] * L
    for i in range(L):
        b[i] = d[i] * w[i]
    return b
