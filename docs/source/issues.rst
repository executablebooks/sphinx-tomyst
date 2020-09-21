Conversion Issues
=================

There are some cases where conversion is not possible due to information
being lost during the initial parsing of the RST document.

Roles
-----

index
~~~~~

The inline ``:index:`` cannot be inferred from the ``sphinx.ast``

.. code-block:: rst

    Is this the same :index:`some text <single: paragraph>`

has the following xml structure

.. code-block:: xml

    <paragraph>
        Is this the same
        <index entries="('single',\ 'paragraph',\ 'index-1',\ '',\ None)">
        <target ids="index-1">
        some text

and the index doesn't wrap ``some text`` that is contained in the original
rst role.

A ``warning`` is issued to identify the document and line number.

.. TODO::

    Consider adding markup such as ``<index>`` to help identify within line
    placement

It appears that the index role is inline for
`deprecation in sphinx=4.0 <https://github.com/sphinx-doc/sphinx/blob/cbc16eb384a0fc6181a4543c34977e794cae231d/sphinx/roles.py#L578>`__


Directives
----------

code-block
~~~~~~~~~~

Given the ``:dedent:`` action is already applied to the associated ``Text``
element it will **not** need to be added as an option in `myst` output.
Therefore the resulting ``myst`` document will not contain the ``:dedent:``
option.
