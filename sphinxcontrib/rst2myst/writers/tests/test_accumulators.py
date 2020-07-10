"""
Tests for writers.accumulators
"""

from sphinxcontrib.rst2myst.writers.accumulators import List

def test_simple():
    a = List()
    a.add_item("first")
    a.add_item("second")
    print(a.to_markdown())

def test_manual_nested():
    a = List()
    a.add_item("first item level 0")
    b = List()
    b.add_item("first item of first item (level 0)")
    c = List()
    c.add_item("first item of (first item of (first item level 0))")
    b.add_item(c)
    a.add_item(b)
    a.add_item("second item level 0")
    d = List()
    d.add_item("first item of second item (level 0)")
    d.add_item("second item of second item (level 0)")
    a.add_item(d)
    print(a.to_markdown())

def test_nested():
    a = List()
    a.add_item("first item level 0")
    a = List(parent=a)
    a.add_item("first item of (first item level 0)")
    a = List(parent=a)
    a.add_item("first item of (first item of (first item level 0))")
    a = a.add_to_parent()
    a = a.add_to_parent()    
    a.add_item("second item level 0")
    a = List(parent=a)
    a.add_item("first item of (second item level 0)")
    a.add_item("second item of (second item level 0)")
    a = a.add_to_parent()
    print(a.to_markdown())


def test_multiline():
    a = List()
    a.add_item("first item level 0\nand second line continuation to first item")
    a.add_item("second item level 0\n\nwith new paragraph")
    a.add_item("third item")
    print(a.to_markdown())

def test_multiline_nested():
    a = List()
    a.add_item("first item level 0\nand second line continuation to first item")
    a = List(parent=a)
    a.add_item("second item level 0\n\nwith new paragraph")
    a = a.add_to_parent()
    print(a.to_markdown())

if __name__ == "__main__":
    print("Simple")
    test_simple()
    print("---------------")
    print("Nested (Manual)")
    test_manual_nested()
    print("---------------")
    print("Nested (Automatic)")
    test_nested()
    print("---------------")
    print("multiline")
    test_multiline()
    print("---------------")
    print("multiline nested")
    test_multiline_nested()