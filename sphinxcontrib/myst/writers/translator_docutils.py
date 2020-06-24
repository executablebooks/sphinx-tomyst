"""
Docutils Methods for Myst Translator

This class is NOT MEANT to operate in ISOLATION.
It documents nodes for the Myst Translator that
are provided by docutils. Sphinx Nodes take precedence

"""

from docutils import nodes

from .accumulators import List, TableBuilder

class MystDocutils:
    """
    Myst Translator Methods for Docutils Nodes

    # References
    Elements: https://docutils.sourceforge.io/docs/ref/doctree.html
    """

    # Docutils Elements

    # Docutils: https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions

    # docutils.admonitions [:class:, :name:]
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#admonitions

    def visit_attention(self, node):
        raise NotImplementedError

    def visit_caution(self, node):
        raise NotImplementedError

    def visit_danger(self, node):
        raise NotImplementedError

    def visit_error(self, node):
        raise NotImplementedError

    def visit_hint(self, node):
        raise NotImplementedError

    def visit_important(self, node):
        raise NotImplementedError

    def visit_note(self, node):
        self.note = True
        self.output.append(self.syntax.visit_note())

    def depart_note(self, node):
        self.note = False

    def visit_tip(self, node):
        raise NotImplementedError

    def visit_warning(self, node):
        raise NotImplementedError

    def visit_admonition(self, node):
        raise NotImplementedError

    # docutils.elements.attribution
    # https://docutils.sourceforge.io/docs/ref/doctree.html#attribution

    def visit_attribution(self, node):
        self.attribution = True
        self.output.append(self.syntax.visit_attribution())

    def depart_attribution(self, node):
        self.attribution = False
        self.add_newline()

    # docutils.elements.caption
    # https://docutils.sourceforge.io/docs/ref/doctree.html#caption

    def visit_caption(self, node):
        self.caption = True
        if self.literal_block['in']:
            raise nodes.SkipNode

    def depart_caption(self, node):
        self.caption = False
        if self.toctree:
            self.output.append("\n")

    # docutils.elements.comment
    # https://docutils.sourceforge.io/docs/ref/doctree.html#comment

    def visit_comment(self, node):
        raise nodes.SkipNode

    # docutils.elements.compound
    # https://docutils.sourceforge.io/docs/ref/doctree.html#compound

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

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
        pass #TODO: remove? use SphinxTranslator version

    def depart_definition_list_item(self, node):
        pass #TODO: remove? use SphinxTranslator version

    # docutils.elements.doctest-block
    # https://docutils.sourceforge.io/docs/ref/doctree.html#doctest-block

    def visit_doctest_block(self, node):
        pass #TODO: remove? use SphinxTranslator version

    def depart_doctest_block(self, node):
        pass #TODO: remove? use SphinxTranslator version

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

    # docutils.elements.footnote
    # https://docutils.sourceforge.io/docs/ref/doctree.html#footnote

    def visit_footnote(self, node):
        self.footnote['in'] = True

    def depart_footnote(self, node):
        self.footnote['in'] = False

    # docutils.container.inline
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
        if self.footnote['in']:
            ids = node.parent.attributes["ids"]
            id_text = ""
            for id_ in ids:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
            self.output.append("<a id='{}'></a>\n**[{}]** ".format(id_text, node.astext())) #TODO: can this be harmonized with HTML
            raise nodes.SkipNode

        if self.citation['in']:
            self.output.append(self.syntax.visit_label())

    def depart_label(self, node):
        if self.citation['in']:
            self.output.append(self.syntax.depart_label())
            self.add_space()

    # docutils.elements.line
    # https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#line-blocks

    def visit_line(self, node):
        pass  #TODO: remove? use SphinxTranslator version

    def depart_line(self, node):
        pass

    def visit_line_block(self, node):
        pass #TODO: remove? use SphinxTranslator version

    def depart_line_block(self, node):
        pass

    # docutils.lists
    # https://docutils.sourceforge.io/docs/ref/doctree.html#bullet-list

    def visit_bullet_list(self, node):
        if not self.List:
            self.List = List(level=0,markers=dict())
        self.List.increment_level()

    def depart_bullet_list(self, node):
        if self.List is not None:
            self.List.decrement_level()
        if self.List and self.List.level == 0:
            markdown = self.List.to_markdown()
            self.output.append(markdown)
            self.List = None

    # https://docutils.sourceforge.io/docs/ref/doctree.html#enumerated-list

    def visit_enumerated_list(self, node):
        if not self.List:
            self.List = List(level=0,markers=dict())
        self.List.increment_level()

    def depart_enumerated_list(self, node):
        if self.List is not None:
            self.List.decrement_level()

        if self.List.level == 0:
            markdown = self.List.to_markdown()
            self.output.append(markdown)
            self.List = None

    def visit_list_item(self, node):
        if self.List:
            self.List.set_marker(node)

    #List(End)

    # ------------------- #
    # Docutils Directives #
    # ------------------- #

    # docutils.block_quote
    # epigraph, highlights, pull_quote

    def visit_block_quote(self, node):
        self.block_quote['in'] = True
        if "epigraph" in node.attributes["classes"]:
            self.block_quote['block_quote_type'] = "epigraph"
        if self.List:
            self.add_newline()
            return
        self.output.append(self.syntax.visit_block_quote())

    def depart_block_quote(self, node):
        if "epigraph" in node.attributes["classes"]:
            self.block_quote['block_quote_type'] = "block-quote"
        self.block_quote['in'] = False
        self.add_newline()

    # docutils.citations
    # https://docutils.sourceforge.io/docs/ref/rst/directives.html#citations

    def visit_citation(self, node):
        self.citation['in'] = True
        if "ids" in node.attributes:
            id_text = ""
            for id_ in node.attributes["ids"]:
                id_text += "{} ".format(id_)
            else:
                id_text = id_text[:-1]
        self.output.append(self.syntax.visit_citation(id_text))

    def depart_citation(self, node):
        self.citation['in'] = False

    # docutils.image
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
        self.figure = {}