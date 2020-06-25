"""
Sphinx Methods for Myst Translator

This class is NOT MEANT to operate in ISOLATION.
It documents nodes for the Myst Translator that
are provided by Sphinx.

"""

from docutils import nodes

from .accumulators import List, TableBuilder

class MystSphinx:
    """
    Myst Translator Methods for Sphinx Nodes
    """

    # sphinx.elements.compact_paragraph
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html?highlight=compact_paragraph#sphinx.addnodes.compact_paragraph

    def visit_compact_paragraph(self, node):
        # TODO: check valid node
        try:
            if node.attributes['toctree']:
                self.toctree = True
        except:
            pass  #Should this execute visit_compact_paragragh in BaseTranslator?

    def depart_compact_paragraph(self, node):
        # TODO: check valid node
        try:
            if node.attributes['toctree']:
                self.toctree = False
        except:
            pass

    # sphinx.directive.index
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#index-generating-markup

    def visit_index(self, node):
        self.index = True

    def depart_index(self, node):
        self.index=False

    # sphinx.directive.only
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-only

    def visit_only(self, node):
        pass  #TODO: can this be removed in favour of default method

    def depart_only(self, node):
        pass