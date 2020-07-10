from typing import Any, Dict, Generator, List, Iterable, Optional, Set, Tuple, Union

from sphinx.application import Sphinx

from .builders import MystBuilder

def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(MystBuilder)

    # app.add_config_value('text_sectionchars', '*=-~"+`', 'env')
    # app.add_config_value('text_newlines', 'unix', 'env')
    # app.add_config_value('text_add_secnumbers', True, 'env')
    # app.add_config_value('text_secnumber_suffix', '. ', 'env')

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }