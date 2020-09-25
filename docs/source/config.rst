Configuration options
=====================

The following sphinx configuration options which you can use in
your ``conf.py`` file are:

.. contents::

General
-------

tomyst_static_file_path
~~~~~~~~~~~~~~~~~~~~~~~

An array which takes path of your static folders, relative to the project's ``confdir``.
It creates the directory structure of the path, inside the output directory: ``_build/myst``;
and then copies over the files inside the given path.

**Usage:**

For config variable:

``tomyst_static_file_path: ["source/_static"]``,

the contents of this folder will be copied over to ``_build/myst/source/_static``.


Target Parser Configuration
---------------------------

tomyst_parser
~~~~~~~~~~~~~

Allows you to choose which parser to target for `myst`

.. list-table:: Title
   :header-rows: 1

   * - Values
     - Default
   * - ``myst_nb``
     - *
   * - ``myst_parser``
     -

The main difference between the two options is how `code` is converted.
When targeting `myst_nb` executable code is contained
in ``code-cell`` directives to enable compatibility with `jupytext` conversion
and code execution.

.. note::

    In the future we would like to support ``jupyter-book`` conversion directly
    by constructing `_config.yml` and `_toc.yml` files.

**Usage:**

.. code-block:: bash

   tomyst_parser = 'myst_parser'

tomyst_jupytext_header
~~~~~~~~~~~~~~~~~~~~~~

This option allows you to specify a custom `jupytext header <https://myst-nb.readthedocs.io/en/latest/use/markdown.html>`__
to support jupytext compatibility and execution using `myst-nb <https://github.com/executablebooks/MyST-NB>`__

This is prepended to the top of every file.

The `default values used by the extension <https://github.com/QuantEcon/sphinx-tomyst/blob/4bdcee8d1dca6d4c80147abc03aa617945495cd5/sphinx_tomyst/__init__.py#L8>`__

Code and Execution
------------------

tomyst_default_language
~~~~~~~~~~~~~~~~~~~~~~~

Allows you to specify the default programming language ["python" is the default otherwise].

This is used to determine if ``code-blocks`` should be included as executable ``code-cells`` or not.
For a code-block that is different to the default programming language (or language synonym) then it
will be added to the generated myst file as display code only.

**Usage:**

.. code-block:: bash

   tomyst_default_language = "julia"

tomyst_language_synonyms
~~~~~~~~~~~~~~~~~~~~~~~~

Allows you to specify multiple names for code that can be executed using the **same** jupyter kernel.

**Default values:** ``ipython``, ``ipython3``, ``python3``

Generated (conf.py) Settings:
-----------------------------

tomyst_conf_removeblocks
~~~~~~~~~~~~~~~~~~~~~~~~

Enables the removal of blocks in the ``conf.py`` using the following block tags.

#. ``tomyst-remove-start``
#. ``tomyst-remove-finish``

These keys can be added as comments and anything between them will be removed.

The **default value:** False

.. warning::

    No checks are implemented for ``start`` / ``finish`` pairs

**Usage:**

.. code-block:: python

   tomyst_conf_removeblocks = True

tomyst_conf_dropcontaining
~~~~~~~~~~~~~~~~~~~~~~~~~~

Enables the removal of a line in the ``conf.py`` based on a pattern.

For example you may want to remove a current package during conversion

.. code-block:: python

   tomyst_conf_dropcontaining = "sphinxcontrib.jupyter"
