"""
sphinxcontrib-tomyst.builders.myst
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A MyST Sphinx Builder

:copyright: Copyright 2020 by the QuantEcon team, see AUTHORS
:licences: see LICENSE for details
"""

import re
from typing import Dict, Iterator, Set, Tuple
from os import path
from sphinx.util.fileutil import copy_asset

from docutils.io import StringOutput
from docutils.nodes import Node

from sphinx.util import logging
from sphinx.util.fileutil import copy_asset_file
from sphinx.builders import Builder
from sphinx.locale import __
from sphinx.util.osutil import ensuredir, os_path

from ..writers import MystWriter, MystTranslator

logger = logging.getLogger(__name__)


class MystBuilder(Builder):

    name = "myst"
    format = "markdown(myst)"
    out_suffix = ".md"
    epilog = __("The myst files are in %(outdir)s.")

    allow_parallel = True
    default_translator_class = MystTranslator

    current_docname = None  # type: str

    def init(self) -> None:
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
        destination = StringOutput(encoding="utf-8")
        self.writer.write(doctree, destination)
        src_folder = self.srcdir.split(self.confdir)[1][1:]
        outdir = path.join(self.outdir, src_folder)
        outfilename = path.join(outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with open(outfilename, "w", encoding="utf-8") as f:
                f.write(self.writer.output)
        except OSError as err:
            logger.warning(__("error writing file %s: %s"), outfilename, err)

    def copy_build_files(self):
        """Copies Makefile and conf.py to _build/myst."""
        import io

        # makefile = path.join(self.confdir, "Makefile")
        src_conf = path.join(self.confdir, "conf.py")
        dest_conf = path.join(self.outdir, "conf.py")

        copy_asset_file(self.confdir + "/Makefile", self.outdir)
        # Update conf.py file with appropriate package import
        if self.config["tomyst_parser"] == "myst_nb":
            pkg = "myst_nb"
        else:
            pkg = "myst_parser"
        # Update conf.py
        drop_items = self.config["tomyst_conf_dropcontaining"]
        block_remove = False
        with io.open(src_conf, "r") as inpf, io.open(dest_conf, "w") as outf:
            for line in inpf.readlines():
                if self.config["tomyst_conf_removeblocks"]:
                    if "tomyst-remove-start" in line:
                        block_remove = True
                    if "tomyst-remove-finish" in line:
                        block_remove = False
                        continue  # so this line doesn't get added
                if not block_remove:
                    if "sphinxcontrib.tomyst" in line:
                        line = line.replace("sphinxcontrib.tomyst", pkg)
                    for item in drop_items:
                        if re.search(item, line):
                            line = ""
                    outf.write(line)

    def copy_static_files(self):
        if "tomyst_static_file_path" in self.config:
            for static_path in self.config["tomyst_static_file_path"]:
                output_path = path.join(self.outdir, static_path)
                ensuredir(output_path)
                entry = path.join(self.confdir, static_path)
                copy_asset(entry, output_path)

    def finish(self):
        self.finish_tasks.add_task(self.copy_static_files)
        self.finish_tasks.add_task(self.copy_build_files)
