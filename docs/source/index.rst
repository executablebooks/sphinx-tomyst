Welcome to sphinx-tomyst's documentation!
=========================================

`sphinx-tomyst <https://github.com/QuantEcon/sphinx-tomyst>`__ is
a Sphinx extension that enables projects to be converted to a `myst <https://myst-parser.readthedocs.io/en/latest/using/syntax.html>`__
project.

Myst files can be compiled using:

#. `myst_nb <https://myst-nb.readthedocs.io/en/latest/>`__, or
#. `myst_parser <https://myst-parser.readthedocs.io/en/latest/>`__, or
#. `Jupyter Book <https://jupyterbook.org/intro.html>`__ (requires manual configuration)

.. note::

   ``sphinx-tomyst`` is currently built to target `myst_nb <https://myst-nb.readthedocs.io/en/latest/>`__
   by **default** but for static projects you can also target
   `myst_parser <https://myst-parser.readthedocs.io/en/latest/>`__ using the
   :ref:`target_parser option <tomyst_parser>`.


Installation
------------

**Step 1:** To install the extension you need to clone the repository then run:

.. code-block:: bash

   python setup.py install

**Step 2:** Add ``sphinx_tomyst`` to your sphinx ``extensions`` in the ``conf.py``

**Step 3:** Build using ``make myst``

.. note::

   A `pypi release<https://github.com/QuantEcon/sphinx-tomyst/issues/75>`__ is
   coming once an `alpha` milestone is reached.



.. toctree::
   :maxdepth: 2
   :hidden:

   config
   contribute
   issues
