Snippet
=======

Another snippet test

<<<<<<< HEAD
    ``import numpy as np``
=======
.. code-block:: python3
    :class: no-execute

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5
>>>>>>> master
