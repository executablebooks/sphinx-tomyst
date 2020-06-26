"""
myst-parser.tests.test_sphinx

Uses sphinx's pytest fixture to run builds

usage:

.. code-block:: python

    @pytest.mark.sphinx(
        buildername='html',
        srcdir='path/to/source')
    def test_basic(app, status, warning, get_sphinx_app_output):

        app.build()

        assert 'build succeeded' in status.getvalue()  # Build succeeded
        warnings = warning.getvalue().strip()
        assert warnings == ""

        output = get_sphinx_app_output(app, buildername='html')

parameters available to parse to ``@pytest.mark.sphinx``:

- buildername='myst'
- srcdir=None
- testroot='root' (only used if srcdir not set)
- freshenv=False
- confoverrides=None
- status=None
- warning=None
- tags=None
- docutilsconf=None

"""
import os
import pathlib
import shutil

import pytest
from sphinx.testing.path import path

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "source"))

# TODO autouse not working, may need to be in root conftest
# (ideally _build folder should be in tempdir)
# @pytest.fixture(scope="session", autouse=True)
@pytest.fixture()
def remove_sphinx_builds():
    """ remove all build directories from the test folder
    """
    yield
    srcdirs = pathlib.Path(SOURCE_DIR)
    for entry in srcdirs.iterdir():  # type: pathlib.Path
        if entry.is_dir() and entry.joinpath("_build").exists():
            shutil.rmtree(str(entry.joinpath("_build")))


@pytest.fixture
def get_sphinx_app_output(file_regression):
    def read(
        app,
        buildername="myst",
        files=["index.myst"],
        encoding="utf-8",
        regress=False
    ):
        contents = []

        for filename in files:
            outpath = path(os.path.join(str(app.srcdir), "_build", buildername, filename))
            if not outpath.exists():
                raise IOError("no output file exists: {}".format(outpath))
            header = "-"*len(filename) + "\n"
            title = header + f"{filename}\n" + header + "\n"
            doc = title + outpath.read_text(encoding=encoding)
            contents.append(doc)

        if regress:
            content = "\n".join(contents)
            file_regression.check(content, extension=".myst")

        return content

    return read


@pytest.fixture
def get_sphinx_app_doctree(file_regression):
    def read(app, docname="index", resolve=False, regress=False):
        if resolve:
            doctree = app.env.get_and_resolve_doctree(docname, app.builder)
            extension = ".resolved.xml"
        else:
            doctree = app.env.get_doctree(docname)
            extension = ".xml"

        # convert absolute filenames
        for node in doctree.traverse(lambda n: "source" in n):
            node["source"] = pathlib.Path(node["source"]).name

        if regress:
            file_regression.check(doctree.pformat(), extension=extension)

        return doctree

    return read
