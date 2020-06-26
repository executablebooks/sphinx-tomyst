
import os
import pytest

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "source"))

@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "basic"), freshenv=True
)
def test_basic(
    app,
    status,
    warning,
    get_sphinx_app_doctree,
    get_sphinx_app_output,
    remove_sphinx_builds,
):
    """basic test."""
    app.build()

    assert "build succeeded" in status.getvalue()  # Build succeeded
    warnings = warning.getvalue().strip()
    assert warnings == ""

    #Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="index", regress=True)
    get_sphinx_app_output(app, files=["index.myst", "test.myst"], regress=True)