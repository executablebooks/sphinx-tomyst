.. sphinxcontrib-tomyst documentation master file, created by
   sphinx-quickstart on Wed Jul  8 15:41:25 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to sphinxcontrib-tomyst's documentation!
================================================

`sphinxcontrib-tomyst <https://github.com/QuantEcon/sphinxcontrib-tomyst>`__ is
a Sphinx extension that enables projects to be converted to `myst <https://myst-parser.readthedocs.io/en/latest/using/syntax.html>`__.

.. image:: https://readthedocs.org/projects/sphinxcontrib-tomyst/badge/?version=latest
   :target: https://sphinxcontrib-tomyst.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Myst files can be compiled using:

#. `myst_nb <https://myst-nb.readthedocs.io/en/latest/>`__, or
#. `myst_parser <https://myst-parser.readthedocs.io/en/latest/>`__, or
#. `Jupyter Book <https://jupyterbook.org/intro.html>`__ (requires manual configuration)

Installation
------------

**Step 1:** To install the extension you need to clone the repository then run:

.. code-block:: bash

   python setup.py install

**Step 2:** Add ``sphinxcontrib.tomyst`` to your sphinx ``extensions`` in the ``conf.py``

**Step 3:** Build using ``make myst``

.. toctree::
   :maxdepth: 2
   :hidden:

   config
   contribute
   issues

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
