"""
Translator for RST to MYST Conversion

TODO:
1. Given the way SphinxTranslator works we should remove all unecessary methods
https://github.com/sphinx-doc/sphinx/blob/275d93b5068a4b6af4c912d5bebb2df928416060/sphinx/util/docutils.py#L438

"""

from __future__ import unicode_literals
import re
import nbformat.v4
from docutils import nodes, writers
from shutil import copyfile
import copy
import os
import time
from collections import OrderedDict

from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .myst import MystSyntax
from .accumulators import List, TableBuilder
from .translator_docutils import MystDocutils
from .translator_sphinx import MystSphinx

logger = logging.getLogger(__name__)

class MystTranslator(MystSphinx, MystDocutils, SphinxTranslator):
    """ Myst Translator
    MystSphinx -> methods for sphinx provided nodes
    MystDocutils -> methods for docutils provided nodes
    """

    # Attribution => MystDocutils
    attribution = False
    # Block Quote (epigraph, highlights, pull_quote) => MystDocutils
    block_quote = dict()
    block_quote['in'] = False
    block_quote['block_quote_type'] = "block-quote"      #TODO: can this be removed?
    # Caption => MystDocutils
    caption = False
    # Citation => MystDocutils
    citation = dict()
    citation['in'] = False
    # Download => MystDocutils
    download_reference = dict()
    download_reference['in'] = False
    # Figure => MystDocutils
    figure = dict()
    # Section => MystDocutils
    section_level = 0
    # Footnote => MystDocutils
    footnote = dict()
    footnote['in'] = False
    footnote_reference = dict()
    footnote_reference['in'] = False
    # Image => MystDocutils
    image = dict()
    # Index => MystSphinx
    index = False
    # List => MystDocutils
    List = None
    # Literal Block => MystDocutils
    literal_block = dict()
    literal_block['in'] = False
    literal_block['no-execute'] = False
    literal_block['hide-output'] = False
    # Math => MystDocutils
    math = dict()
    math['in'] = False
    math_block = dict()
    math_block['in'] = False
    math_block['math_block_label'] = None
    # Note => MystDocutils
    note = False
    # References => MystDocutils
    reference_text_start = 0
    inpage_reference = False
    # Rubric => MystDocutils
    rubric = False
    # Tables => MystDocutils
    Table = None
    # Text => MystDocutils
    text = None
    # Titles => MystDocutils
    visit_first_title = True
    title = ""
    # Toctree => MystDocutils  #TODO: Should this work be done in MystSphinx?
    toctree = False
    # Topic => MystDocutils
    topic = False

    # Static Asset Trackers
    images = []
    files = []
    cached_state = dict()   #A dictionary to cache states to support nested blocks
    URI_SPACE_REPLACE_FROM = re.compile(r"\s")
    URI_SPACE_REPLACE_TO = "-"

    def __init__(self, document, builder):
        """
        A Myst(Markdown) Translator
        """
        super().__init__(document, builder)
        #-Syntax-#
        self.syntax = MystSyntax()
        # DEBUG
        self.language = "python"
        self.language_synonyms = ["ipython"]
        self.default_ext = ".myst"

    #-Document-#

    def visit_document(self, node):
        self.output = []

    def depart_document(self, node):
        self.body = "".join(self.output)

    #-Nodes-#

    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

    def unknown_departure(self, node):
        pass

    #Output Formatting Utilities

    def add_space(self, n=1):
        self.output.append(" " * n)

    def add_newline(self, n=1):
        self.output.append("\n" * n)

    def add_newparagraph(self):
        self.output.append("\n\n")

    # TODO: Review Utilities below

    @classmethod
    def split_uri_id(cls, uri):
        regex = re.compile(r"([^\#]*)\#?(.*)")
        return re.search(regex, uri).groups()

    @classmethod
    def add_extension_to_inline_link(cls, uri, ext):
        """
        Removes an extension such as `html` and replaces with `ipynb`

        .. todo::

            improve implementation for references (looks hardcoded)
        """
        if "." not in uri:
            if len(uri) > 0 and uri[0] == "#":
                return uri
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)
        #adjust relative references
        elif "../" in uri:
            # uri = uri.replace("../", "")
            uri, id_ = cls.split_uri_id(uri)
            if len(id_) == 0:
                return "{}{}".format(uri, ext)
            else:
                return "{}{}#{}".format(uri, ext, id_)

        return uri

    @staticmethod
    def strip_blank_lines_in_end_of_block(line_text):
        lines = line_text.split("\n")

        for line in range(len(lines)):
            if len(lines[-1].strip()) == 0:
                lines = lines[:-1]
            else:
                break

        return "\n".join(lines)

    # Myst Support
    @staticmethod
    def myst_options(options):
        """ return myst options block

        #TODO: add support for returning shorthand options syntax
        # if there are less than or equal to 2 options specified
        """
        myst_options = []
        myst_options.append("---")
        for item in sorted(options.keys()):
            myst_options.append('{}: {}'.format(item, options[item]))
        myst_options.append("---")
        if len(myst_options) == 2:
            myst_options = []
        return myst_options
