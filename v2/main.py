from pprint import pprint

import numpy as np

from v2.base import generate_states


if __name__ == '__main__':
    L = 3
    H = 4
    limits = [(1, 3), (2, 3), (2, 4)]
    mu = [0.5, 1., 0.7]
    Theta = np.array([
        [0., 0.7, 0.3],
        [0.2, 0., 0.8],
        [0.5, 0.5, 0.]
    ])

    states = generate_states(L, H)
    pprint(states)
    print("states len list", len(states))

