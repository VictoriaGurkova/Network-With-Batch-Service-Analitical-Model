from collections import namedtuple
from pprint import pprint

import numpy as np

from v2.base import generate_states, generate_d, generate_a, generate_Y

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

    states = generate_states(L, H)
    pprint(states)
    print("states list len:", len(states))

    Y = generate_Y(limits)
    pprint(Y)
    print("Y len:", len(Y))
