Configuration options
=====================

The configuration options specific to ``tomyst`` which you can use in your ``conf.py`` file are:

**tomyst_parser**:

Allows you to choose which parser to target for `myst` (`myst_parser`, `myst_nb`).

The default is `myst_nb`

The main difference is how `code` is converted. When targeting `myst_nb` executable code is contained
in ``code-cell`` directives to enable `jupytext` conversion and code execution.

**tomyst_static_file_path**:

An array which takes path of your static folders, relative to the project's ``confdir``. It creates the directory structure of the path, inside the output directory: ``_build/myst``; and then copies over the files inside the given path.

*Example*:

For config variable: ``tomyst_static_file_path: ["source/_static"]``, the contents of this folder will be copied over to ``_build/myst/source/_static``.

**tomyst_jupytext_header**:

Can specify a custom `jupytext header <https://myst-nb.readthedocs.io/en/latest/use/markdown.html>`__
to support jupytext compatibility and execution using `myst-nb <https://github.com/executablebooks/MyST-NB>`__

Control of Code
---------------

**tomyst_default_language:**

The default programming language (default = "python").

This is used to determine if code should be included as executable or not. For a code-block that is
different to the default programming language (or language synonym) then it will be added to the
generated myst file as display code only.

**tomyst_language_synonyms:**

Enables multiple names for code that can be executed on the **same** jupyter kernel.

Default values are: ``ipython, ipython3, python3``

Control over Generated (conf.py):
---------------------------------

**tomyst_conf_removeblocks:**

Enables the removal of blocks in the ``conf.py`` using following block tags.

#. ``tomyst-remove-start``
#. ``tomyst-remove-finish``

These keys can be added as comments and anything between them will be removed.

.. warning::

    No checks are implemented for ``start`` / ``finish`` pairs

**tomyst_conf_dropcontaining:**

Enables the remove of a line in the conf based on a pattern.
