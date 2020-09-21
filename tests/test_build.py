
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

    get_sphinx_app_doctree(app, docname="test", regress=True)
    get_sphinx_app_output(app, files=["index.md", "test.md"], regress=True)

@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "docutils"), freshenv=True
)
def test_docutils(
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

    #Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="elements", regress=True)
    get_sphinx_app_output(app, files=["index.md", "elements.md", "directives.md", "roles.md"], regress=True)

@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "extended"), freshenv=True
)
def test_extended(
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

    get_sphinx_app_doctree(app, docname="test", regress=True)
    get_sphinx_app_output(app, files=["index.md", "test.md"], regress=True)


@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "jupytext-header"), freshenv=True
)
def test_jupytext(
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

    #Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="content", regress=True)
    get_sphinx_app_output(app, files=["index.md", "content.md"], regress=True)

@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "multi-lang"), freshenv=True
)
def test_multi_language(
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

    #Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="test", regress=True)
    get_sphinx_app_output(app, files=["index.md", "test.md"], regress=True)

@pytest.mark.sphinx(
    buildername="myst", srcdir=os.path.join(SOURCE_DIR, "multi-lang-jupytext"), freshenv=True
)
def test_multi_language_jupytext(
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

    #Note: pytest needs to run twice to initialise fixtures

    get_sphinx_app_doctree(app, docname="test", regress=True)
    get_sphinx_app_output(app, files=["index.md", "test.md"], regress=True)