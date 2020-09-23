Snippet
=======

Another snippet test

skip-test

.. code-block:: python3
    :class: skip-test

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5

hide-output

.. code-block:: python3
    :class: hide-output

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5

both

.. code-block:: python3
    :class: skip-test, hide-output

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5
