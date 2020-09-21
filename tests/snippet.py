import os
import pytest

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "source"))


@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "snippet"), freshenv=True
)
def test_snippet(
    app,
    status,
    warning,
    get_sphinx_app_output,
    # remove_sphinx_builds,
):
    """basic test."""
    app.build()
    output = get_sphinx_app_output(app, files=["snippet.md"], regress=True)
    print(output)
