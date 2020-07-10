"""
sphinxcontrib-rst2myst.builders.myst
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A MyST Sphinx Builder

:copyright: Copyright 2020 by the QuantEcon team, see AUTHORS
:licences: see LICENSE for details
"""

from typing import Any, Dict, Iterator, Set, Tuple
from os import path

from docutils.io import StringOutput
from docutils.nodes import Node

from sphinx.util import logging
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util.osutil import ensuredir, os_path

from ..writers import MystWriter, MystTranslator

logger = logging.getLogger(__name__)

class MystBuilder(Builder):

    name = 'myst'
    format = 'markdown(myst)'
    out_suffix = ".md"
    epilog = __('The myst files are in %(outdir)s.')

    allow_parallel = True
    default_translator_class = MystTranslator

    current_docname = None # type: str

    def init(self) -> None:
        # import pdb; pdb.set_trace()
        self.secnumbers = {}  # type: Dict[str, Tuple[int, ...]]

    def get_outdated_docs(self) -> Iterator[str]:
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = path.join(self.outdir, docname + self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except OSError:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except OSError:
                pass

    def get_target_uri(self, docname: str, typ: str = None) -> str:
        return docname

    def prepare_writing(self, docnames: Set[str]) -> None:
        self.writer = MystWriter(self)

    def write_doc(self, docname: str, doctree: Node) -> None:
        self.current_docname = docname
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with open(outfilename, 'w', encoding='utf-8') as f:
                f.write(self.writer.output)
        except OSError as err:
            logger.warning(__("error writing file %s: %s"), outfilename, err)

    def finish(self):
        pass
