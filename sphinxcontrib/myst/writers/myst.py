"""
Myst Syntax
"""

from .markdown import MarkdownSyntax

class MystSyntax(MarkdownSyntax):
    
    def visit_admonition(self, title):
        return "```{{admonition}} {}".format(title)

    def depart_admonition(self):
        return "```"

    def visit_literal_block(self, language=None):
        if language is None:
            return "```"
        else:
            return "```{{code-block}} {0}".format(language)

    def visit_target(self, target):
        return "({})=".format(target)

    def visit_figure(self, uri, options=None):
        if options is None:
            return "```{{figure}} {}".format(uri)
        else:
            options = "\n".join(options)
            return "```{{figure}} {}\n{}".format(uri, options)

    def depart_figure(self):
        return "```"

    def visit_note(self):
        return "```{{note}} "

    def depart_note(self):
        return "```"