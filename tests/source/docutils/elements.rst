Elements
========

:Author: Random Hacker
:Contact: jrh@example.com
:Date: 2002-08-18
:Status: Work In Progress
:Version: 1
:Filename: $RCSfile$
:Copyright: This document has been placed in the public domain.
:Address: 123 Example Ave.
          Example, EX

This document contains test cases for elements that
are **not** directives.

Text
----

This is some text

.. _block_quote:

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

definition_list
---------------

This tests ``definition``, ``definition_list`` and
``definition_list_item``

Term
  Definition.

Term : classifier
    The ' : ' indicates a classifier in
    definition list item terms only.

docinfo
-------

See docinfo elements at the top of this document
just underneath the first title.

They don't appear to be transformed by sphinx/docutils
to be `docinfo` elements.

https://github.com/mmcky/sphinx-tomyst/issues/19

emphasis
--------

This is *emphasis* markup text

enumerated_list
---------------

The enumerated list from docutils

1. Item 1.

   (A) Item A.
   (B) Item B.
   (C) Item C.

2. Item 2.


target Links
------------

See :ref:`block quote section <block_quote>` above
