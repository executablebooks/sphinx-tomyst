"""
Attribute Recovery Tools

Note: Work in Progress to see if making objects is more efficient

"""

class Attributes:
    interface = {}
    exclude = {}

    def __init__(self, node):
        self.node = node
        self.option_names = self.interface.keys()
        self.extract_options()
        self.process_exclude()

    def extract_options(self):
        self.options = {}
        for option in self.option_names:
            attr = self.interface[option]
            if self.node.hasattr(attr):
                self.options[option] = self.node.attributes[attr]

    def process_exclude(self):
        for item in self.exclude.keys():
            if item in self.options and self.options[item] in self.exclude[item]:
                self.options.remove(item)

    def myst(self):
        """return myst representation of infered options"""
        pass

class FigureAttributes(Attributes):
    interface = {
        'align'     : 'align',
        'figwidth'  : 'width',
        'figclass'  : 'classes',
    }
    exclude = {
        'align'     : ['default'],
        'figclass'  : [],
    }
