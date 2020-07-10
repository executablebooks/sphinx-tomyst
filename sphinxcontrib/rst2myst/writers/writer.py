from docutils import nodes, writers
from typing import cast

from .translator import MystTranslator

class MystWriter(writers.Writer):
    supported = ('myst',)
    settings_spec = ('No options here.', '', ())
    settings_defaults = {}  # type: Dict

    output = None  # type: str

    def __init__(self, builder: "MystBuilder") -> None:
        super().__init__()
        self.builder = builder

    def translate(self) -> None:
        visitor = self.builder.create_translator(self.document, self.builder)
        self.document.walkabout(visitor)
        self.output = cast(MystTranslator, visitor).body