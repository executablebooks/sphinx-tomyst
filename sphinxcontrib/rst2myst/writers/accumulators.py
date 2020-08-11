"""
Provides accumulator objects to assist with building Syntax
"""

from docutils import nodes

class ListBuilder:

    marker = "*"
    indentation = " "*2
    item_count = 0
    level = 0

    def __init__(self, marker):
        self.items = []
        self.set_marker(marker)

    def visit_list(self):
        self.level += 1

    def depart_list(self):
        self.level -= 1

    def set_marker(self, marker):
        if marker is not None:
            self.marker = marker

    def add_item(self, content):
        self.item_count += 1
        item = {
            'level' : self.level,
            'content' : content,
            'item_count' : self.item_count,
            'marker' : self.marker,
        }
        self.items.append(item)

    def to_markdown(self):
        markdown = []
        for item in self.items:
            indent = self.indentation * item['level']
            marker = item['marker']
            offset = indent + " "*len(marker) + " "
            content = item['content'].replace("\n", "\n{}".format(offset))
            markdown.append("{}{} {}".format(indent, marker, content))
        return "\n".join(markdown)

# class ListCollector:

#     def __init__(self, marker="*"):
#         self.lists = []
#         self.current = SimpleList(marker)

#     def visit_list(self, marker="*"):
#         self.lists.append(self.current)
#         level = self.current.level
#         self.current = SimpleList(level=level)

#     def to_markdown(self):
#         markdown = []
#         for item in self.lists:
#             markdown.append(item.to_markdown())

class List:

    list_item = None
    level = 0
    indentation = " "*4  #4 space indentation as default commonmark
    item_count = 0
    from_child = False
    marker = "*"
    parent = None

    def __init__(self, marker=None, parent='base'):
        """
        List Accumulator
        Consists of <items> and <List> objects to define
        markdown syntax

        Example
        -------
        from markdown import List
        a = List()
        a.add_item("first")
        a.add_item("second")
        a.to_markdown()
        """
        self.items = []
        if marker:
            self.marker = marker
        self.parent = parent
        if type(parent) is List:
            self.level += parent.level + 1
            self.item_count = parent.item_count

    def __repr__(self):
        return self.to_markdown()

    def start_list_item(self):
        self.list_item = []

    def addto_list_item(self, content):
        if self.list_item is None:
            self.start_list_item()
        self.list_item.append(content)

    def add_list_item(self):
        content = "".join(self.list_item)
        content = self.parse_paragraphs(content)
        self.add_item(content)
        self.list_item = None

    def parse_paragraphs(self, content):
        #-Paragraph Markers-#
        content = content.rstrip("<\\paragraph>")
        content = content.replace("<\\paragraph>", "\n\n")
        return content

    def add_item(self, item):
        """
        Add Item to List

        Parameters
        ----------
        item : str or List
        """
        # Support for Unpacking Recursion
        if self.from_child:
            self.items.append(item)
            self.from_child = False
        else:
            # Support for Building from Independent Objects
            if type(item) is List:
                item.increment_level()
            else:
                content = item
                item = {
                    'content'   : content,
                    'level'     : self.level,
                    'marker'    : self.marker,
                    'item_count' : self.item_count,
                }
            self.items.append(item)
            self.item_count += 1

    def to_markdown(self):
        markdown = []
        for item in self.items:
            if type(item) is List:
                markdown.append(item.to_markdown())
            else:
                indent = self.indentation * item['level']
                marker = item['marker']
                offset = indent + " "*len(marker) + " "
                content = item['content'].replace("\n", "\n{}".format(offset))
                markdown.append("{}{} {}".format(indent, marker, content))
        return "\n".join(markdown)

    def increment_level(self):
        self.level += 1
        for item in self.items:
            if type(item) is List:
                item.level += 1
            else:
                item['level'] += 1

    def decrement_level(self):
        self.level -= 1
        for item in self.items:
            if type(item) is List:
                item.level -= 1
            item['level'] -= 1

    def add_to_parent(self):
        if type(self.parent) is List:
            self.parent.from_child = True
            self.parent.add_item(self)
            return self.parent

#-Table Builder-#

class TableBuilder:

    align = "center"
    def __init__(self, node):
        self.table = []
        self.current_line = 0
        self.lines = []
        self.row = ""
        self.column_widths = []
        if 'align' in node:
            self.align = node['align']

    def __repr__(self):
        return self.to_markdown()

    def start_row(self):
        self.row = "|"

    def add_item(self, text):
        self.row += text + "|"

    def end_row(self):
        self.row += "\n"
        self.lines.append(self.row)
        self.row = ""

    def add_title(self, node):
        self.lines.append("### {}\n".format(node.astext()))

    def add_column_width(self, colwidth):
        self.column_widths.append(colwidth)

    def generate_alignment_line(self, line_length, alignment):
        left = ":" if alignment != "right" else "-"
        right = ":" if alignment != "left" else "-"
        return left + "-" * (line_length - 2) + right

    def add_header_line(self, header_line):
        for col_width in self.column_widths:
            header_line += self.generate_alignment_line(
                col_width, self.align)
            header_line += "|"
        self.lines.append(header_line + "\n")

    def to_markdown(self):
        """
        converts the table items to markdown
        """
        return "".join(self.lines)
