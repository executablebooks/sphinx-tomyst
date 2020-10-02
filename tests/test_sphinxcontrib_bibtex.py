import os
import pytest

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "source"))


@pytest.mark.sphinx(
    buildername="myst",
    srcdir=os.path.join(SOURCE_DIR, "sphinxcontrib-bibtex"),
    freshenv=True,
)
def test_sphinxcontrib_bibtex(
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

    # Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="test", regress=True)
    get_sphinx_app_output(
        app, files=["index.md", "test.md", "references.md"], regress=True
    )
