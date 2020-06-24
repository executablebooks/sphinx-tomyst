"""
Sphinx Methods for Myst Translator

This class is NOT MEANT to operate in ISOLATION.
It documents nodes for the Myst Translator that
are provided by Sphinx.

"""

class MystSphinx:
    """
    Myst Translator Methods for Sphinx Nodes
    """
    
    # sphinx.directive.index
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#index-generating-markup

    def visit_index(self, node):
        self.index = True

    def depart_index(self, node):
        self.index=False