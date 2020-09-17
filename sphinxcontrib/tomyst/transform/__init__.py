"""
Transform to Intercept Sphinx AST before transforms/post-transforms
"""

from sphinx.transforms import SphinxTransform
from sphinx.util import logging

logger = logging.getLogger(__name__)


def intercept_ast(config, document, tags):
    document.document_pretransforms = document.deepcopy()


class InterceptAST(SphinxTransform):

    default_priority = 1

    def apply(self):
        intercept_ast(self.config, self.document, self.app.builder.tags)
