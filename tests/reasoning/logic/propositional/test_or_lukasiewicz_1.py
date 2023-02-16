##
# Copyright 2023 IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
##

from lnn import Proposition, Or, Model
import numpy as np


def test():
    """Unittest for upward 2-input real-value disjunction"""

    samples = 21
    steps = np.linspace(0, 1, samples)
    x, y = np.meshgrid(steps, steps)

    # define the rules
    A = Proposition("A")
    B = Proposition("B")
    AB = Or(A, B)

    # rules per model
    formulae = [AB]

    for row in range(samples):
        for col in range(samples):
            # inputs
            a, b = x[row][col], y[row][col]

            # ground truth
            GT = min(a + b, 1)

            # facts per model
            facts = {A: (a, a), B: (b, b)}

            # load data into a new model
            model = Model()
            model.add_knowledge(*formulae)
            model.add_data(facts)

            # evaluate the disjunction
            AB.upward()

            # test the prediction
            prediction = AB.get_data()[0]
            assert (
                prediction - GT <= 1e-7
            ), f"And({a}, {b}) expected {GT}, received {prediction}"


if __name__ == "__main__":
    test()
