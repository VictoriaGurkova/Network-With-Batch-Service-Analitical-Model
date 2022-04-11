from collections import namedtuple
from pprint import pprint

import numpy as np

from v2.base import generate_states, generate_Y, get_generator, get_stationary_distribution, \
    get_omega, generate_d
from v2.measures import get_d_i, mean_customs_num, response_time, waiting_in_queue, mean_customs_in_queue

if __name__ == '__main__':
    L = 3
    H = 4

    Limit = namedtuple("Limit", ["x", "y"])
    limits = [Limit(1, 3), Limit(2, 3), Limit(2, 4)]
    mu = [0.5, 1., 0.7]
    Theta = np.array([
        [0., 0.7, 0.3],
        [0.2, 0., 0.8],
        [0.5, 0.5, 0.]
    ])

    print("states:")
    states = generate_states(L, H)
    pprint(states)
    print("states list len:", len(states))

    print("generator:")
    generator = get_generator(states, limits, mu, Theta)
    pprint(generator)

    print("pi:")
    pi = get_stationary_distribution(generator)
    pprint(pi)
    print(sum(pi))

    print("state with pi:")
    StateAndPi = namedtuple("StateAndPi", ["state", "pi"])
    states_to_pi = [StateAndPi(states[i], pi[i]) for i in range(len(states))]
    pprint(states_to_pi)

    print("d_set:")
    d_set = generate_d(limits)
    pprint(d_set)
    print("d_set len:", len(d_set))

    print("Y:")
    Y = generate_Y(limits)
    pprint(Y)
    print("Y len:", len(Y))

    print("omega:")
    omega = get_omega(L, Theta)
    print(omega)
    print("sum omega:", sum(omega))

    print("d:")
    # змаенили Y на d_set
    d = [get_d_i(i, H, Y, states_to_pi, states, generator, omega) for i in range(L)]
    print(d)

    s = mean_customs_num(L, H, states_to_pi)
    print("М. о. числа требований в системах:", s, sum(s), end='\n' * 2)

    u = response_time(L, s, d)
    print("М. о. длительности пребывания требований в системе:", u, end='\n' * 2)

    w = waiting_in_queue(L, u, mu)
    print("М. о. длительности пребывания требований в очереди системы:", w, end='\n' * 2)

    b = mean_customs_in_queue(L, d, w)
    print("М. о. числа требований в очереди:", b, end='\n' * 2)
