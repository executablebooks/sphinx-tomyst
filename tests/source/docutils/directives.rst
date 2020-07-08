Directives
==========

This document contains directive test cases

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

caution
-------

.. caution::

   This is a caution admonition

danger
------

.. danger::

   This is a danger admonition

epigraph
--------

.. epigraph::

   No matter where you go, there you are.

   -- Buckaroo Banzai

figure
------

TBD


highlights
----------

.. highlights::

    This is a highlights directive

index
-----

.. index:: python

.. index:: python, programming

A point in the text you'd like to reference something
about python

.. index::
   single: python
   single: programming
   :name: reference-id

A point in the text you'd like to reference something
about python

.. index::
   single: execution; context

The execution context
---------------------

pull-quote
----------

.. pull-quote::

    This is a pull-quote directive

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

math
----

.. math:: (a + b)^2 = a^2 + 2ab + b^2

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

.. math::
   :label: math-label

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2


.. math::
   :label: math-label2
   :nowrap:

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

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