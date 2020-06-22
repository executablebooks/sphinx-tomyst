"""
Myst Syntax
"""

from .markdown import MarkdownSyntax

class MystSyntax(MarkdownSyntax):
    
    def visit_literal_block(self, language=None):
        if language is None:
            return "```"
        else:
            return "```{{code-block}} {0}".format(language)

    def visit_target(self, target):
        return "({})=".format(target)