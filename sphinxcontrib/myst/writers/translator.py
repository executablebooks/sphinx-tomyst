"""
Translator for RST to MYST Conversion

TODO:
1. Given the way SphinxTranslator works we should remove all unecessary methods
https://github.com/sphinx-doc/sphinx/blob/275d93b5068a4b6af4c912d5bebb2df928416060/sphinx/util/docutils.py#L438

"""

from __future__ import unicode_literals
import re
from docutils import nodes, writers
from shutil import copyfile
import copy
import os
import time
from collections import OrderedDict

from sphinx.util import logging
from sphinx.util.docutils import SphinxTranslator

from .myst import MystSyntax
from .accumulators import List
from .accumulators import TableBuilder

logger = logging.getLogger(__name__)

class MystTranslator(SphinxTranslator):
    """ Myst Translator

    docutils:
        1. https://docutils.sourceforge.io/docs/ref/doctree.html
        2. https://docutils.sourceforge.io/docs/ref/doctree.html#element-reference
    sphinx:
        1. https://www.sphinx-doc.org/en/master/extdev/nodes.html
        2. https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html

    .. todo::
        1. review NotImplementedError to see if visit methods in base classes
           are suitable
    """

    indentation = " " * 2

    # Boolean(State Tracking)
    admonition = False
    attribution = False
    attention = False
    caption = False
    caution = False
    citation = False
    danger = False
    download_reference = False
    error = False
    footnote = False
    hint = False
    important = False
    literal_block = False
    math = False
    note = False
    inpage_reference = False
    tip = False
    toctree = False
    topic = False
    warning = False

    # Dict(State Tracking)
    # Block Quote
    block_quote = dict()
    block_quote['in'] = False
    block_quote['type'] = None
    # Figure
    figure = dict()
    figure['in'] = False
    figure['figure-options'] = None
    # Footnote Reference
    footnote_reference = dict()
    footnote_reference['in'] = False
    footnote_reference['link'] = None
    # Bullet List
    bullet_list = dict()
    bullet_list['in'] = True
    bullet_list['marker'] = "*"
    bullet_list['level'] = -1
    # Math
    math_block = dict()
    math_block['in'] = False
    math_block['label'] = None

    # Accumulators
    List = None
    Table = None

    def __init__(self, document, builder):
        """
        A Myst(Markdown) Translator
        """
        super().__init__(document, builder)
        self.syntax = MystSyntax()
        self.default_ext = ".myst"
        self.images = []
        self.section_level = 0

    #----------#
    #-Document-#
    #----------#

    def visit_document(self, node):
        self.output = []

    def depart_document(self, node):
        self.body = "".join(self.output)

    def unknown_visit(self, node):
        raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

    def unknown_departure(self, node):
        pass

    #-------#
    #-Nodes-#
    #-------#

    # -- Text -- #

    def visit_Text(self, node):
        text = node.astext()

        #Escape Special markdown chars except in code block
        if self.block_quote['in'] and self.block_quote['type'] == 'block_quote':
            linemarker = self.syntax.visit_block_quote()
            text = linemarker + text
            text = text.replace("\n", "\n{}".format(linemarker))
        if self.caption:
            raise nodes.SkipNode
        #Inline Math
        if self.math:
            text = self.syntax.visit_math(text.strip())
        #Math Blocks
        elif self.math_block['in'] and self.math_block['label']:
            text = self.syntax.visit_math_block(text.strip(), self.math_block['label'])
            self.math_block['label'] = None
        elif self.math_block['in']:
            text = self.syntax.visit_math_block(text.strip())
        #Code Blocks
        # if self.literal_block:
            # text = self.strip_whitespace(text)

        self.text = text

    def depart_Text(self, node):
        if self.List:
            self.List.addto_list_item(self.text)
            return
        if self.Table:
            self.Table.add_item(self.text)
            return
        if self.math_block['in']:
            self.text = self.text + "\n\n"
        if self.literal_block:
            self.text = self.text + "\n"
        if self.caption and self.toctree:         #TODO: Check this condition
            self.text = "# {}".format(self.text)
        self.output.append(self.text)

    # -- Elements --- #

    # docutils.elements.abbreviation
    # https://docutils.sourceforge.io/docs/ref/doctree.html#abbreviation

    # docutils.elements.acroynm
    # https://docutils.sourceforge.io/docs/ref/doctree.html#acronym

    # docutils.elements.address
    # https://docutils.sourceforge.io/docs/ref/doctree.html#address

    # docutils.elements.admonition
    # types: attention, caution, danger, error, hint, important, note, tip, warning
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions

    def visit_admonition(self, node):
        self.admonition = True
        title = self.infer_admonition_attrs(node)
        if title is None:
            raise SyntaxWarning("title attribute cannot be None")
        syntax = self.syntax.visit_admonition(title)
        self.output.append(syntax)
        self.add_newline()

    def infer_admonition_attrs(self, node):
        title = None
        for child in node.children:
            if type(child) is nodes.title:
                title = child.astext()
        return title

    def depart_admonition(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_admonition())
        self.add_newparagraph()
        self.admonition = False

    # docutils.elements.attention
    # https://docutils.sourceforge.io/docs/ref/doctree.html#attention

    def visit_attention(self, node):
        self.attention = True
        self.output.append(self.syntax.visit_directive("attention"))
        self.add_newline()

    def depart_attention(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.attention = False

    # docutils.elements.attribution
    # https://docutils.sourceforge.io/docs/ref/doctree.html#attribution

    def visit_attribution(self, node):
        self.attribution = True
        self.add_newline()
        self.output.append(self.syntax.visit_attribution())

    def depart_attribution(self, node):
        self.attribution = False
        self.add_newline()

    # docutils.elements.author
    # https://docutils.sourceforge.io/docs/ref/doctree.html#author
    # https://docutils.sourceforge.io/docs/ref/doctree.html#authors

    # docutils.element.block_quote
    # class types: epigraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#block-quote

    def visit_block_quote(self, node):
        self.block_quote['in'] = True
        if self.List:           #TODO: can you have block quote in List?
            pass
            # self.add_newline()
            # return
        # Determine class type
        if "epigraph" in node.attributes["classes"]:
            self.block_quote['type'] = "epigraph"
            self.output.append(self.syntax.visit_directive("epigraph"))
            self.add_newline()
        elif "highlights" in node.attributes["classes"]:
            self.block_quote['type'] = "highlights"
            self.output.append(self.syntax.visit_directive("highlights"))
            self.add_newline()
        elif "pull-quote" in node.attributes["classes"]:
            self.block_quote['type'] = "pull-quote"
            self.output.append(self.syntax.visit_directive("pull-quote"))
            self.add_newline()
        else:
            self.block_quote['type'] = "block_quote"

    def depart_block_quote(self, node):
        if self.block_quote['type'] != "block_quote":
            self.output.append(self.syntax.depart_directive())
            self.add_newparagraph()
        self.block_quote['in'] = False

    # docutils.elements.bullet_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#bullet-list

    def visit_bullet_list(self, node):
        marker = None
        if node.hasattr("bullet"):
            marker = node.attributes['bullet']
        if not self.List:
            self.List = List(marker=marker)
        else:
            #Finalise any open List Item
            if self.List.list_item:
                self.List.add_list_item()
            self.List = List(marker=marker, parent=self.List)

    def depart_bullet_list(self, node):
        if self.List.parent == 'base':
            self.output.append(self.List.to_markdown())
            self.add_newparagraph()
            self.List = None
        else:
            self.List = self.List.add_to_parent()

    # docutils.elements.caption
    # https://docutils.sourceforge.io/docs/ref/doctree.html#caption

    def visit_caption(self, node):
        self.caption = True
        if self.literal_block:
            raise nodes.SkipNode

    def depart_caption(self, node):
        self.caption = False
        if self.toctree:
            self.output.append("\n")

    # docutils.elements.caution
    # https://docutils.sourceforge.io/docs/ref/doctree.html#caution

    def visit_caution(self, node):
        self.caution = True
        self.output.append(self.syntax.visit_directive("caution"))
        self.add_newline()

    def depart_caution(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.caution = False

    # docutils.citations
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#citations

    def visit_citation(self, node):
        self.citation = True
        if "ids" in node.attributes:
            id_text = ""
            for id_ in node.attributes["ids"]:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
        self.output.append(self.syntax.visit_citation(id_text))

    def depart_citation(self, node):
        self.citation = False

    # docutils.elements.citation_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#citation-reference

    # docutils.elements.classifier
    # https://docutils.sourceforge.io/docs/ref/doctree.html#classifier

    # docutils.elements.colspec
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#colspec

    def visit_colspec(self, node):
        self.Table.add_column_width(node['colwidth'])

    # docutils.elements.comment
    # https://docutils.sourceforge.io/docs/ref/doctree.html#comment

    def visit_comment(self, node):
        raise nodes.SkipNode

    # sphinx.nodes.compact_paragraph
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html?highlight=compact_paragraph#sphinx.addnodes.compact_paragraph

    def visit_compact_paragraph(self, node):
        pass #TODO: review

    def depart_compact_paragraph(self, node):
        pass

    # docutils.elements.compound
    # https://docutils.sourceforge.io/docs/ref/doctree.html#compound

    def visit_compound(self, node):
        if "toctree-wrapper" in node['classes']:
            self.toctree = True

    def depart_compound(self, node):
        if "toctree-wrapper" in node['classes']:
            self.toctree = False

    # docutils.elements.contact
    # https://docutils.sourceforge.io/docs/ref/doctree.html#contact

    # docutils.elements.container
    # https://docutils.sourceforge.io/docs/ref/doctree.html#container

    def visit_container(self, node):
        pass

    def depart_container(self, node):
        pass

    # docutils.elements.copyright
    # https://docutils.sourceforge.io/docs/ref/doctree.html#copyright

    # docutils.elements.danger
    # https://docutils.sourceforge.io/docs/ref/doctree.html#danger

    def visit_danger(self, node):
        self.danger = True
        self.output.append(self.syntax.visit_directive("danger"))
        self.add_newline()

    def depart_danger(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.danger= False

    # docutils.elements.date
    # https://docutils.sourceforge.io/docs/ref/doctree.html#date

    # docutils.elements.decoration
    # https://docutils.sourceforge.io/docs/ref/doctree.html#decoration

    # docutils.elements.definition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition

    def visit_definition(self, node):
        self.output.append(self.syntax.visit_definition())
        self.add_newline()

    def depart_definition(self, node):
        self.output.append(self.syntax.depart_definition())
        self.add_newline()

    # docutils.elements.definition_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition-list

    def visit_definition_list(self, node):
        self.add_newline()
        self.output.append(self.syntax.visit_definition_list())
        self.add_newline()

    def depart_definition_list(self, node):
        self.add_newline()
        self.output.append(self.syntax.depart_definition_list())
        self.add_newparagraph()

    # docutils.elements.definition_list_item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#definition-list-item

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    # docutils.elements.description
    # https://docutils.sourceforge.io/docs/ref/doctree.html#description

    # docutils.elements.docinfo
    # https://docutils.sourceforge.io/docs/ref/doctree.html#docinfo

    # docutils.elements.doctest-block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#doctest-block

    def visit_doctest_block(self, node):
        pass #TODO: remove? use SphinxTranslator version

    def depart_doctest_block(self, node):
        pass

    # docutils.elements.document
    # https://docutils.sourceforge.io/docs/ref/doctree.html#document

    # sphinx.nodes.download_reference
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#new-inline-nodes

    def visit_download_reference(self, node):
        self.download_reference = True
        html = "<a href={} download>".format(node["reftarget"])
        self.output.append(html)

    def depart_download_reference(self, node):
        self.download_reference = False
        self.output.append("</a>")

    # docutils.elements.emphasis
    # uses: Text
    # https://docutils.sourceforge.io/docs/ref/doctree.html#emphasis

    def visit_emphasis(self, node):
        if self.List:
            self.List.addto_list_item(self.syntax.visit_italic())
        else:
            self.output.append(self.syntax.visit_italic())

    def depart_emphasis(self, node):
        if self.List:
            self.List.addto_list_item(self.syntax.depart_italic())
        else:
            self.output.append(self.syntax.depart_italic())


    # docutils.elements.entry
    # uses: table?
    # https://docutils.sourceforge.io/docs/ref/doctree.html#entry

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    # docutils.elements.enumerated_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#enumerated-list

    def visit_enumerated_list(self, node):
        """
        .. TODO: should use item_count to make a more readable
        list in markdown output
        """
        marker = "1."
        if not self.List:
            self.List = List(marker=marker)
        else:
            #Finalise any open List Item
            if self.List.list_item:
                self.List.add_list_item()
            self.List = List(marker=marker, parent=self.List)

    def depart_enumerated_list(self, node):
        if self.List.parent == 'base':
            self.output.append(self.List.to_markdown())
            self.add_newparagraph()
            self.List = None
        else:
            self.List = self.List.add_to_parent()

    # docutils.elements.error
    # https://docutils.sourceforge.io/docs/ref/doctree.html#error

    def visit_error(self, node):
        self.error = True
        self.output.append(self.syntax.visit_directive("error"))
        self.add_newline()

    def depart_error(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.error= False

    # docutils.elements.field
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field

    def visit_field(self, node):
        for child in node.children:
            if type(child) is nodes.field_name:
                field_name = child.astext()
            elif type(child) is nodes.field_body:
                field_body = child.astext()
        raise NotImplementedError

    # docutils.elements.field_body
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-body

    def visit_field_body(self, node):
        self.visit_definition(node)  #TODO: review if wrapper of definition

    def depart_field_body(self, node):
        self.depart_definition(node)

    # docutils.elements.field_list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-list

    def visit_field_list(self, node):
        self.visit_definition_list(node)  #TODO: review if wrapper of definition

    def depart_field_list(self, node):
        self.depart_definition_list(node)

    # docutils.element.field_name
    # https://docutils.sourceforge.io/docs/ref/doctree.html#field-name

    def visit_field_name(self, node):
        self.visit_term(node)

    def depart_field_name(self, node):
        self.depart_term(node)

    # docutils.figure
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#figure

    def visit_figure(self, node):
        """
        Note: additional options need parsing in image node
        """
        self.figure['in'] = True
        self.figure['figure-options'] = self.infer_figure_attrs(node)

    def infer_figure_attrs(self, node):
        """
        :align: -> align
        :figwidth: -> width
        :figclass: -> classes
        """
        options = {}
        if node.hasattr("align"):
            align = node.attributes["align"]
            if align not in ["default"]:  #if not set may have default value = default
                options['align'] = align
        if node.hasattr("width"):
            options['figwidth'] = node.attributes["width"]
        if len(node.attributes["classes"]) > 0:
            classes = str(node.attributes["classes"]).strip('[]').strip("'")
            options['figclass'] = classes
        return options

    def depart_figure(self, node):
        self.figure['in'] = False
        self.figure['figure-options'] = None

    # docutils.elements.footer
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footer

    # docutils.elements.footnote
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footnote

    def visit_footnote(self, node):
        self.footnote = True

    def depart_footnote(self, node):
        self.footnote = False

    # docutils.elements.footnote_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footnote-reference

    def visit_footnote_reference(self, node):
        self.footnote_reference['in'] = True
        refid = node.attributes['refid']
        ids = node.astext()
        self.footnote_reference['link'] = "<sup>[{}](#{})</sup>".format(ids, refid) #TODO: can this be harmonized with HTML
        self.output.append(self.footnote_reference['link'])
        raise nodes.SkipNode

    def depart_footnote_reference(self, node):
        self.footnote_reference['in'] = False

    # docutils.elements.generated
    # https://docutils.sourceforge.io/docs/ref/doctree.html#generated

    # docutils.elements.header
    # https://docutils.sourceforge.io/docs/ref/doctree.html#header

    # docutils.elements.hint
    # https://docutils.sourceforge.io/docs/ref/doctree.html#hint

    def visit_hint(self, node):
        self.hint = True
        self.output.append(self.syntax.visit_directive("hint"))
        self.add_newline()

    def depart_hint(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.hint= False

    # docutils.elements.image
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#images

    def visit_image(self, node):
        """
        1. the scale, height and width properties are not combined in this
        implementation as is done in http://docutils.sourceforge.net/docs/ref/rst/directives.html#image
        """
        options = self.infer_image_attrs(node)
        if self.figure['in']:
            figure_options = self.figure['figure-options']
            options = {**options, **figure_options} #Figure options take precedence
        options = self.myst_options(options)
        uri = node.attributes["uri"]
        self.images.append(uri)
        if self.figure['in']:
            syntax = self.syntax.visit_figure(uri, options)
        else:
            syntax = self.syntax.visit_image(uri, options)
        self.output.append(syntax)

    def infer_image_attrs(self, node):
        """
        https://docutils.sourceforge.io/docs/ref/rst/directives.html#image-options
        :alt: -> alt
        :height: -> height
        :width: -> width
        :scale: -> scale
        :align: -> align
        :target: -> node.parent = docutils.nodes.reference
        """
        options = {}
        for option in ['alt', 'height', 'width', 'scale', 'align']:
            if node.hasattr(option):
                options[option] = node.attributes[option]
        if type(node.parent) is nodes.reference:
            if node.parent.hasattr('refuri'):
                options['target'] = node.parent.attributes['refuri']
        return options

    def depart_image(self, node):
        self.add_newline()
        self.output.append(self.syntax.depart_figure())
        self.add_newparagraph()

    # docutils.elements.important
    # https://docutils.sourceforge.io/docs/ref/doctree.html#important

    def visit_important(self, node):
        self.important = True
        self.output.append(self.syntax.visit_directive("important"))
        self.add_newline()

    def depart_important(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.important= False

    # sphinx.nodes.index
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#new-inline-nodes
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#index-generating-markup

    def visit_index(self, node):
        pass

    def depart_index(self, node):
        pass

    # docutils.elements.inline
    # uses: container?
    # https://docutils.sourceforge.io/docs/ref/doctree.html#inline

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    # docutils.container.label
    # https://docutils.sourceforge.io/docs/ref/doctree.html#label

    def visit_label(self, node):
        """
        Notes: footnote requires `html` to create links within the
        notebooks as there is no markdown equivalent
        """
        if self.footnote:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            self.output.append("<a id='{}'></a>\n**[{}]** ".format(id_text, node.astext())) #TODO: can this be harmonized with HTML
            raise nodes.SkipNode

        if self.citation:
            self.output.append(self.syntax.visit_label())

    def depart_label(self, node):
        if self.citation:
            self.output.append(self.syntax.depart_label())
            self.add_space()

    # docutils.elements.legend
    # https://docutils.sourceforge.io/docs/ref/doctree.html#legend

    # docutils.elements.line
    # https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#line-blocks

    def visit_line(self, node):
        pass  #TODO: remove? use SphinxTranslator version

    def depart_line(self, node):
        pass

    # docutils.elements.line_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#line-block

    def visit_line_block(self, node):
        pass #TODO: remove? use SphinxTranslator version

    def depart_line_block(self, node):
        pass

    # docutils.elements.list_item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#list-item

    def visit_list_item(self, node):
        self.List.start_list_item()

    def depart_list_item(self, node):
        if self.List.list_item:
            self.List.add_list_item()

    # docutils.element.literal
    # https://docutils.sourceforge.io/docs/ref/doctree.html#literal

    def visit_literal(self, node):
        if self.download_reference:
            return            #TODO: can we just raise SkipNode?

        if self.List:
            self.List.addto_list_item(self.syntax.visit_literal())
        else:
            self.output.append(self.syntax.visit_literal())

    def depart_literal(self, node):
        if self.download_reference:
            return

        if self.List:
            self.List.addto_list_item(self.syntax.depart_literal())
        else:
            self.output.append(self.syntax.depart_literal())

    # docutils.element.literal_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#literal-block

    def visit_literal_block(self, node):
        self.literal_block = True
        options = self.infer_literal_block_attrs(node)
        self.nodelang = node.attributes["language"].strip()
        syntax = self.syntax.visit_literal_block(self.nodelang)
        #option block parsing
        if options != []:
            options = "\n".join(options)
            syntax = syntax + "\n" + options
        if self.List:
            self.List.addto_list_item(syntax)
            self.List.addto_list_item("\n")
        else:
            self.output.append(syntax)
            self.add_newline()

    def infer_literal_block_attrs(self, node):
        """
        :dedent: option cannot be inferred as text is already altered
        but could be a PR upstream in
        sphinx/directives/code.py -> literal['dedent'] = self.options['dedent']
        """
        attributes = node.attributes
        options = []
        options.append("---")
        if node.hasattr('linenos') and attributes['linenos']:
            options.append("linenos:")
        if node.hasattr('highlight_args'):
            if 'linenostart' in attributes['highlight_args']:
                options.append("lineno-start: {}".format(attributes['highlight_args']['linenostart']))
            if 'hl_lines' in attributes['highlight_args']:
                vals = str(attributes['highlight_args']['hl_lines']).strip('[]')
                options.append("emphasize-lines: {}".format(vals))
        if type(node.parent) is nodes.container:
            if node.parent.hasattr('names'):
                vals = str(node.parent.attributes['names']).strip('[]').strip("'")
                options.append("name: {}".format(vals))
            # Check children for caption
            for child in node.parent.children:
                if type(child) is nodes.caption:
                    caption = child.astext()
                    options.append("caption: {}".format(caption))
        if node.hasattr("force") and attributes['force']:
            options.append("force:")
        options.append("---")
        if len(options) == 2:
            options = []
        return options

    def depart_literal_block(self, node):
        syntax = self.syntax.depart_literal_block()
        if self.List:
            self.List.addto_list_item("\n")
            self.List.addto_list_item(syntax)
            self.List.addto_list_item("\n")
        else:
            self.output.append(syntax)
            self.add_newparagraph()
        self.literal_block = False

    # docutils.element.math
    # https://docutils.sourceforge.io/docs/ref/doctree.html#math

    def visit_math(self, node):
        """
        Inline Math

        Notes
        -----
        With sphinx < 1.8, a math node has a 'latex' attribute, from which the
        formula can be obtained and added to the text.

        With sphinx >= 1.8, a math node has no 'latex' attribute, which mean
        that a flag has to be raised, so that the in visit_Text() we know that
        we are dealing with a formula.

        TODO:
            1. Deprecate support for sphinx < 1.8
        """
        self.math = True
        try: # sphinx < 1.8
            math_text = node.attributes["latex"].strip()
        except KeyError:
            # sphinx >= 1.8
            # the flag is raised, the function can be exited.
            return                                              #TODO: raise nodes.SkipNode?

        formatted_text = self.syntax.visit_math(math_text)

        if self.Table:
            self.Table.add_item(formatted_text)
        else:
            self.output.append(formatted_text)

    def depart_math(self, node):
        self.math = False

    # docutils.element.math_block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#math-block

    def visit_math_block(self, node):
        """
        Math from Directives

        Notes:
        ------
        visit_math_block is called only with sphinx >= 1.8
        """
        self.math_block['in'] = True
        #check for labelled math
        if node["label"]:
            #Use \tags in the embedded LaTeX environment
            #Haven't included this in self.syntax.MardownSyntax as it should be general across HTML (mathjax), PDF (latex)
            self.math_block['label'] = "\\tag{" + str(node["number"]) + "}\n"

    def depart_math_block(self, node):
        self.math_block['in'] = False

    # docutils.elements.paragraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#paragraph

    # docutils.elements.note
    # https://docutils.sourceforge.io/docs/ref/doctree.html#note

    def visit_note(self, node):
        self.note = True
        self.output.append(self.syntax.visit_directive("note"))
        self.add_newline()

    def depart_note(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.note = False

    # sphinx.nodes.only
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#special-nodes
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-only

    def visit_only(self, node):
        pass  #TODO: can this be removed in favour of default method

    def depart_only(self, node):
        pass

    # docutils.elements.option
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-argument
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-group
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-list
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-list-item
    # https://docutils.sourceforge.io/docs/ref/doctree.html#option-string

    # docutils.elements.organization
    # https://docutils.sourceforge.io/docs/ref/doctree.html#organization

    # docutils.elements.paragraph
    # https://docutils.sourceforge.io/docs/ref/doctree.html#paragraph

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self.List:
            if self.List.list_item:
                self.List.addto_list_item("<\\paragraph>")  #Used for Formating
            return
        if self.block_quote['in'] and self.block_quote['type'] != 'block_quote':
            self.add_newline()
            return
        self.add_newparagraph()

    # docutils.elements.pending
    # https://docutils.sourceforge.io/docs/ref/doctree.html#pending

    # docutils.elements.problematic
    # https://docutils.sourceforge.io/docs/ref/doctree.html#problematic

    def visit_problematic(self, node):
        pass

    def depart_problematic(self, node):
        pass

    # docutils.elements.raw
    # https://docutils.sourceforge.io/docs/ref/doctree.html#raw

    def visit_raw(self, node):
        pass

    def depart_raw(self, node):
        self.add_newparagraph()

    # docutils.elements.references
    # https://docutils.sourceforge.io/docs/ref/doctree.html#reference

    #TODO: rework references
    #TODO: add syntax too MarkdownSyntax, MystSyntax

    def visit_reference(self, node):
        self.reference = True
        if self.List:
            self.List.addto_list_item("[")
        elif self.figure['in']:
            pass
        else:
            self.output.append("[")

    def depart_reference(self, node):
        subdirectory = False
        formatted_text = ""

        if self.topic:
            # Jupyter Notebook uses the target text as its id
            uri_text = node.astext().replace(" ","-")
            formatted_text = "](#{})".format(uri_text)
            #self.output.append(formatted_text)
        else:
            # if refuri exists, then it includes id reference
            if "refuri" in node.attributes:
                refuri = node["refuri"]
                # add default extension(.ipynb)
                if "internal" in node.attributes and node.attributes["internal"] == True:
                    refuri = self.add_extension_to_inline_link(refuri, self.default_ext)
            else:
                # in-page link
                if "refid" in node:
                    refid = node["refid"]
                    self.inpage_reference = True
                    #markdown doesn't handle closing brackets very well so will replace with %28 and %29
                    refid = refid.replace("(", "%28")
                    refid = refid.replace(")", "%29")
                    #markdown target
                    refuri = "#{}".format(refid)
                # error
                else:
                    self.error("Invalid reference")
                    refuri = ""

            #TODO: review if both %28 replacements necessary in this function?
            #      Propose delete above in-link refuri
            #ignore adjustment when targeting pdf as pandoc doesn't parse %28 correctly
            refuri = refuri.replace("(", "%28")  #Special case to handle markdown issue with reading first )
            refuri = refuri.replace(")", "%29")
            formatted_text = "]({})".format(refuri)

        ## if there is a list add to it, else add it to the output
        if self.List:
            self.List.addto_list_item(formatted_text)
        elif self.figure['in']:
            pass
        else:
            self.output.append(formatted_text)

    # docutils.elements.revision
    # https://docutils.sourceforge.io/docs/ref/doctree.html#revision

    # docutils.elements.row
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#row

    def visit_row(self, node):
        self.Table.start_row()

    def depart_row(self, node):
        self.Table.end_row()

    # docutil.elements.rubric
    # https://docutils.sourceforge.io/docs/ref/doctree.html#rubric

    def visit_rubric(self, node):
        if len(node.children) == 1 and node.children[0].astext() in ['Footnotes']:
            self.output.append('**{}**\n\n'.format(node.children[0].astext()))            #TODO: add to MarkdownSyntax?
            raise nodes.SkipNode

    def depart_rubric(self, node):
        pass

    # docutils.elements.section
    # https://docutils.sourceforge.io/docs/ref/doctree.html#section

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1

    # docutils.elements.sidebar
    # https://docutils.sourceforge.io/docs/ref/doctree.html#sidebar

    # docutils.elements.status
    # https://docutils.sourceforge.io/docs/ref/doctree.html#status

    # docutils.elements.strong
    # https://docutils.sourceforge.io/docs/ref/doctree.html#strong

    def visit_strong(self, node):
        if self.List:
            self.List.addto_list_item(self.syntax.visit_bold())
        else:
            self.output.append(self.syntax.visit_bold())

    def depart_strong(self, node):
        if self.List:
            self.List.addto_list_item(self.syntax.depart_bold())
        else:
            self.output.append(self.syntax.depart_bold())

    # docutils.elements.subscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#subscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#substitution-definition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#substitution-reference

    # docutils.elements.subtitle
    # https://docutils.sourceforge.io/docs/ref/doctree.html#subtitle

    # docutils.elements.superscript
    # https://docutils.sourceforge.io/docs/ref/doctree.html#superscript

    # docutils.elements.system_message
    # https://docutils.sourceforge.io/docs/ref/doctree.html#system-message

    # docutils.elements.table
    # Category: Compound
    # https://docutils.sourceforge.io/docs/ref/doctree.html#table

    def visit_table(self, node):
        self.Table = TableBuilder(node)

    def depart_table(self, node):
        markdown = self.Table.to_markdown()
        self.output.append(markdown)
        self.Table = None
        self.add_newline()

    # docutils.elements.target
    # https://docutils.sourceforge.io/docs/ref/doctree.html#target

    def visit_target(self, node):
        if "refid" in node.attributes:
            self.output.append(self.syntax.visit_target(node.attributes["refid"]))
            self.add_newline()

    def depart_target(self, node):
        pass

    # docutils.elements.tbody
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tbody

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    # docutils.element.term
    # https://docutils.sourceforge.io/docs/ref/doctree.html#term

    def visit_term(self, node):
        self.output.append("<dt>")

    def depart_term(self, node):
        self.output.append("</dt>\n")

    # docutils.element.tgroup
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tgroup

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    # docutils.element.thead
    # uses: table
    # https://docutils.sourceforge.io/docs/ref/doctree.html#thead

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        """ create the header line which contains the alignment for each column """
        self.Table.add_header_line("|")

    # docutils.element.tip
    # https://docutils.sourceforge.io/docs/ref/doctree.html#tip

    def visit_tip(self, node):
        self.tip = True
        self.output.append(self.syntax.visit_directive("tip"))
        self.add_newline()

    def depart_tip(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.tip = False

    # docutils.element.title
    # https://docutils.sourceforge.io/docs/ref/doctree.html#title

    def visit_title(self, node):
        if self.admonition:
            raise nodes.SkipNode
        elif self.topic:
            # this prevents from making it a subsection from section
            self.output.append(self.syntax.visit_title(self.section_level + 1))
            self.add_space()
        elif self.Table:
            self.Table.add_title(node)
        else:
            self.output.append(self.syntax.visit_title(self.section_level))
            self.add_space()

    def depart_title(self, node):
        if not self.Table:
            self.add_newparagraph()

    # docutils.element.title_reference
    # https://docutils.sourceforge.io/docs/ref/doctree.html#title-reference

    def visit_title_reference(self, node):
        pass

    def depart_title_reference(self, node):
        pass

    # sphinx.nodes.toctree
    # https://www.sphinx-doc.org/en/master/extdev/nodes.html#sphinx.addnodes.toctree

    def visit_toctree(self, node):
        import pdb; pdb.set_trace()
        self.toctree = True

    def depart_toctree(self, node):
        self.toctree = False

    # docutils.elements.topic
    # https://docutils.sourceforge.io/docs/ref/doctree.html#topic

    def visit_topic(self, node):
        self.topic = True

    def depart_topic(self, node):
        self.topic = False

    # docutils.elements.transition
    # https://docutils.sourceforge.io/docs/ref/doctree.html#transition

    # docutils.elements.version
    # https://docutils.sourceforge.io/docs/ref/doctree.html#version

    # docutils.elements.warning
    # https://docutils.sourceforge.io/docs/ref/doctree.html#warning

    def visit_warning(self, node):
        self.warning = True
        self.output.append(self.syntax.visit_directive("warning"))
        self.add_newline()

    def depart_warning(self, node):
        self.remove_newline()
        self.output.append(self.syntax.depart_directive())
        self.add_newparagraph()
        self.warning = False

    #-----------#
    #-Utilities-#
    #-----------#

    def strip_whitespace(self, text):
        text = text.split("\n")
        text = [item.strip() for item in text]
        return "\n".join(text)

    def add_space(self, n=1):
        self.output.append(" " * n)

    def add_newline(self, n=1):
        self.output.append("\n" * n)

    def remove_newline(self):
        if self.output[-1] == '\n\n':
            self.output[-1] = '\n'
        elif self.output[-1] == '\n':
            self.output.pop()

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
        """
        num_options = len(options.keys())
        myst_options = []
        if num_options == 0:
            return myst_options
        elif num_options < 2:   #TODO parameterise this in conf.py
            for option, option_val in options.items():
                myst_options.append(":{}: {}".format(option, option_val))
            return myst_options
        else:
            myst_options.append("---")
            for item in sorted(options.keys()):
                myst_options.append('{}: {}'.format(item, options[item]))
            myst_options.append("---")
            return myst_options
