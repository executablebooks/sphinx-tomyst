Contribute to sphinx-tomyst
==================================

Welcome to the ``sphinx-tomyst`` repository!

We're excited you're here and want to contribute. ✨

Development guidelines
----------------------

For information about development conventions, practices, and
infrastructure, please see `the executablebooks/ development
guidelines <https://github.com/executablebooks/.github/blob/master/CONTRIBUTING.md>`__.

Getting started
---------------

To get started with the ``sphinx-tomyst`` *codebase*, take the following steps:

Step 1: Clone and install the package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/QuantEcon/sphinx-tomyst.git


Next, install:

::

    pip install -e .[testing,code_style]


This will install ``sphinx-tomyst`` locally, along with the packages needed to test it
as well as packages for ensuring code style.

Step 2: Install the pre-commit hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``sphinx-tomyst`` uses `pre-commit <https://pre-commit.com/>`__ to ensure code style
and quality before a commit is made. This ensures that the look and feel remain consistent
over time and across developers. ``pre-commit`` is installed when you
install sphinx-tomyst with ``pip install -e .[code_style]``.

To enable ``pre-commit`` for your clone, run the following from the repository root:

::

    pre-commit install


From now on, when you make a commit to ``sphinx-tomyst``, ``pre-commit`` will ensure
that your code looks correct according to a few checks.

Step 3: Run the tests
~~~~~~~~~~~~~~~~~~~~~

For code tests, ``sphinx-tomyst`` uses `pytest <https://docs.pytest.org>`_.
You may run all the tests with the following command:

::

    pytest
