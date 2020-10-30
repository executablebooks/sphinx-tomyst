Directives
==========

index
-----

The index directives

.. index::
   single: Python

.. index::
   single: Python
   :name: test1

.. index::
   single: Python; Runtime
   single: Julia

.. index::
   single: Python; Runtime
   single: Julia
   :name: test2

literalinclude
--------------

.. literalinclude:: _static/test.txt

.. literalinclude:: _static/test.txt
   :emphasize-lines: 2
   :linenos:

.. literalinclude:: _static/test.py
   :language: python

only
----

The only directive

.. only:: html

    HTML

.. only:: latex

    LaTeX
