from docutils import writers
from typing import cast, Dict

from ..builders import MystBuilder
from .translator import MystTranslator


class MystWriter(writers.Writer):
    supported = ("myst",)
    settings_spec = ("No options here.", "", ())
    settings_defaults = {}  # type: Dict

    output = None  # type: str

    def __init__(self, builder: "MystBuilder") -> None:
        super().__init__()
        self.builder = builder
        self.PRE_TRANSFORM = True

    def translate(self) -> None:
        if self.PRE_TRANSFORM:
            reporter = self.document.reporter  # save current reporter
            self.document = (
                self.document.document_pretransforms
            )  # pass pre-transforms document to writer
            self.document.reporter = reporter
        visitor = self.builder.create_translator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = cast(MystTranslator, visitor).body
