from typing import Any, Dict

from sphinx.application import Sphinx

from .builders import MystBuilder
from .transform import InterceptAST

DEFAULT_JUPYTEXT_HEADER = """
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
"""


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_builder(MystBuilder)

    app.add_transform(InterceptAST)
    app.add_config_value("tomyst_static_file_path", ['_static'], "tomyst")
    app.add_config_value("tomyst_debug", False, "tomyst")

    #JupyText Compatibility
    app.add_config_value("tomyst_jupytext", False, "tomyst")
    app.add_config_value(
        "tomyst_jupytext_header", DEFAULT_JUPYTEXT_HEADER, "tomyst"
    )  # noqa: E501

    app.add_config_value("tomyst_default_language", "python", "tomyst")
    app.add_config_value("tomyst_language_synonyms", \
      ["ipython", "ipython3", "python2", "python3"], "tomyst")

    return {
        "version": "builtin",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
