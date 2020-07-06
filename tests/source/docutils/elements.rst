Elements
========

Text
----

This is some text

..
   address
   -------

   :Address: 123 Example Ave.
            Example, EX

admonition
----------

Generic admonition requires a title argument to
be provided

.. admonition:: My rst link

   Here is `rst link syntax <https://jupyter.org>`__
   converted to markdown

.. admonition:: title for admonition

   You can make up your own admonition too.

   with some additional lines

attention
---------

.. attention::

   This is an attention admonition

..
   author
   ------

   :Author: J. Random Hacker

..
   authors
   -------

   :Authors: J. Random Hacker; Jane Doe

block_quote
-----------

This is the main document

   This is a block quote context
   with multiple lines

bullet_list
-----------

A simple bullet list

- first item
- second item

A multi-paragraph example

- Item 1, paragraph 1.

  Item 1, paragraph 2.

- Item 2.

A nested bullet list

- first item level 0

  - first item of first item (level 0)

- second item level 0

  - first item of second item (level 0)
  - second item of second item (level 0)

An example with nested code-block

- Step 1. Example:

  .. code-block:: bash

     Example code

- Step 2.

For extended **list** testing please refer
to the `list <list>`__ test page.

caution
-------

.. caution::

   This is a caution admonition

danger
------

.. danger::

   This is a danger admonition

enumerated_list
---------------

The enumerated list from docutils

1. Item 1.

   (A) Item A.
   (B) Item B.
   (C) Item C.

2. Item 2.

error
-----

.. error::

   This is an error admonition

hint
----

.. hint::

   This is a hint admonition

important
---------

.. important::

   This is an important admonition

note
----

.. note::

   This is a note admonition.

   It does not require any arguments

tip
---

.. tip::

   This is a tip admonition

warning
-------

.. warning::

   This is a warning admonition