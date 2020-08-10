from typing import Any, Dict, Generator, List, Iterable, Optional, Set, Tuple, Union

from sphinx.application import Sphinx

from .builders import MystBuilder
from .transform import InterceptAST

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(MystBuilder)

    app.add_transform(InterceptAST)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }