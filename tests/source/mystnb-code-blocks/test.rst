Testing Document
================

This is a document that contains various python code blocks in addition
to non-python code blocks

Python
------

.. code-block::

   import numpy as np

.. code-block:: python

   import numpy as np

.. code-block:: python3

   import numpy as np

.. code-block:: ipython

   import numpy as np

Non-Python
----------

.. code-block:: julia

   Pkg.update()

.. code-block:: none

   Some Plain Text

Options
-------

Test no-execute passthrough to code-blocks

.. code-block:: python
   :class: no-execute

   import numpy as np

Test skip-test passthrough to code-cells

.. code-block:: python
   :class: skip-test

   print(thisfails)

Test hide-output passthrough to code-cells

.. code-block:: python3
    :class: hide-output

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5

.. code-block:: python3
    :class: collapse

    for i in range(40):
      print(i)

Combinations
~~~~~~~~~~~~

.. code-block:: python3
    :class: skip-test, hide-output

    from random import uniform

    samples = [uniform(0, 1) for i in range(10)]
    F = ECDF(samples)
    F(0.5)  # Evaluate ecdf at x = 0.5
