
# flake8: noqa

"""
This Sphinx extension is adapted from discord.py's neo-docs.
It is designed specifically to generate documentation tables
for Read the Docs.
"""

from sphinx.util.docutils import SphinxDirective
from sphinx.locale import _
from docutils import nodes
from sphinx import addnodes

from collections import namedtuple, OrderedDict
import importlib
import inspect
import os
import re


class attributetable(nodes.General, nodes.Element):
    """A node representing an attribute table."""
    pass


class attributetablecolumn(nodes.General, nodes.Element):
    """A node representing a column within an attribute table."""
    pass


class attributetabletitle(nodes.TextElement):
    """A node for the title or label of an attribute table."""
    pass


class attributetableplaceholder(nodes.General, nodes.Element):
    """A placeholder node for the attribute table, used during parsing."""
    pass


class attributetablebadge(nodes.TextElement):
    """A badge node for additional metadata in attribute tables."""
    pass


class attributetable_item(nodes.Part, nodes.Element):
    """A node representing an item in the attribute table list."""
    pass


def visit_attributetable_node(self, node):
    """Handle entering an attributetable node."""
    class_name = node['python-class']
    self.body.append(f'<div class="py-attribute-table" data-move-to-id="{class_name}">')


def visit_attributetablecolumn_node(self, node):
    """Handle entering an attributetablecolumn node."""
    self.body.append(self.starttag(node, 'div', CLASS='py-attribute-table-column'))


def visit_attributetabletitle_node(self, node):
    """Handle entering an attributetabletitle node."""
    self.body.append(self.starttag(node, 'span'))


def visit_attributetablebadge_node(self, node):
    """Handle entering an attributetablebadge node."""
    attributes = {
        'class': 'py-attribute-table-badge',
        'title': node.get('badge-type', 'badge'),
    }
    self.body.append(self.starttag(node, 'span', **attributes))


def visit_attributetable_item_node(self, node):
    """Handle entering an attributetable_item node."""
    self.body.append(self.starttag(node, 'li', CLASS='py-attribute-table-entry'))


def depart_attributetable_node(self, node):
    """Handle leaving an attributetable node."""
    self.body.append('</div>')


def depart_attributetablecolumn_node(self, node):
    """Handle leaving an attributetablecolumn node."""
    self.body.append('</div>')


def depart_attributetabletitle_node(self, node):
    """Handle leaving an attributetabletitle node."""
    self.body.append('</span>')


def depart_attributetablebadge_node(self, node):
    """Handle leaving an attributetablebadge node."""
    self.body.append('</span>')


def depart_attributetable_item_node(self, node):
    """Handle leaving an attributetable_item node."""
    self.body.append('</li>')


_name_parser_regex = re.compile(r'(?P<module>[\w.]+\.)?(?P<name>\w+)')


class PyAttributeTable(SphinxDirective):
    """ A class representing a Sphinx Directive to generate
    attribute tables for documentation using Read the Docs.
    """
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    def parse_name(self, content):
        """ Parses the name to retrieve the module and name.

        Parameters:
        - content: The content string to parse.

        Returns:
        A tuple of (modulename, name).

        Raises:
        - RuntimeError: If modulename cannot be determined.
        """
        path, name = _name_parser_regex.match(content).groups()
        if path:
            modulename = path.rstrip('.')
        else:
            modulename = self.env.temp_data.get('autodoc:module')
            if not modulename:
                modulename = self.env.ref_context.get('py:module')
        if modulename is None:
            raise RuntimeError(f'modulename somehow None for {content} in {self.env.docname}.')

        return modulename, name

    def run(self):
        """ Generates the initial placeholder node for the attribute table.

        The actual HTML generation occurs later when the document tree is
        fully parsed.

        Returns:
        A list containing the placeholder node configured with module
        and class information.
        """
        content = self.arguments[0].strip()
        node = attributetableplaceholder('')
        modulename, name = self.parse_name(content)
        node['python-module'] = modulename
        node['python-class'] = name
        node['python-full-name'] = f'{modulename}.{name}'
        return [node]


def build_lookup_table(env):
    """
    Construct a lookup table from the provided environment.
    The table maps full class names to their members.

    :param env: The sphinx environment.
    :return: A dictionary mapping class fullnames to their associated objects.
    """
    lookup_table = {}
    py_domain = env.domains['py']

    ignored_types = {
        'data', 'exception', 'module', 'class',
    }

    for fullname, _, objtype, docname, _, _ in py_domain.get_objects():
        if objtype in ignored_types:
            continue

        class_fullname, _, member_name = fullname.rpartition('.')
        lookup_table.setdefault(class_fullname, []).append(member_name)

    return lookup_table


TableElement = namedtuple('TableElement', ['fullname', 'label', 'badge'])


def process_attributetable(app, doctree, fromdocname):
    """Process attribute table nodes in the document tree."""
    env = app.builder.env

    lookup = build_lookup_table(env)
    for node in doctree.traverse(attributetableplaceholder):
        modulename = node.get('python-module')
        classname = node.get('python-class')
        fullname = node.get('python-full-name')
        groups = get_class_results(lookup, modulename, classname, fullname)
        table = attributetable('')
        for label, subitems in groups.items():
            if subitems:
                subitems_sorted = sorted(
                    subitems,
                    key=lambda element: (getattr(element.badge, 'rawsource', '') or 'aa') + element.label
                )
                table.append(class_results_to_node(label, subitems_sorted))

        table['python-class'] = fullname
        node.replace_self([table] if table else [])


def get_class_results(lookup, modulename, name, fullname):
    """Retrieve class results from the lookup table and module."""
    try:
        module = importlib.import_module(modulename)
    except ImportError:
        return OrderedDict([(_('Attributes'), []), (_('Methods'), [])])

    cls = getattr(module, name, None)
    if cls is None:
        return OrderedDict([(_('Attributes'), []), (_('Methods'), [])])

    groups = OrderedDict([
        (_('Attributes'), []),
        (_('Methods'), []),
    ])

    try:
        members = lookup[fullname]
    except KeyError:
        return groups

    for attr in members:
        attrlookup = f'{fullname}.{attr}'
        key = _('Attributes')
        badge = None
        label = attr

        value = getattr(cls, attr, None)
        if value is not None:
            doc = value.__doc__ or ''
            if inspect.iscoroutinefunction(value) or doc.startswith('|coro|'):
                key = _('Methods')
                badge = attributetablebadge('await', 'await')
                badge['badge-type'] = _('coroutine')
            elif isinstance(value, classmethod):
                key = _('Methods')
                label = f'{name}.{attr}'
                badge = attributetablebadge('cls', 'cls')
                badge['badge-type'] = _('classmethod')
            elif inspect.isfunction(value) and doc.startswith(('A decorator', 'A shortcut decorator')):
                badge = attributetablebadge('@', '@')
                badge['badge-type'] = _('decorator')
                key = _('Methods')
            elif inspect.isfunction(value):
                key = _('Methods')

        if key == _('Methods'):
            label += '()'

        groups[key].append(TableElement(fullname=attrlookup, label=label, badge=badge))

    return groups


def class_results_to_node(category, items):
    header = attributetabletitle(category, category)
    bullet_list = nodes.bullet_list('')
    for item in items:
        ref_node = nodes.reference('', '', internal=True,
                                   refuri='#' + item.fullname,
                                   anchorname='',
                                   *[nodes.Text(item.label)],
                                   classes=['py-attribute-table-name'])
        paragraph = addnodes.compact_paragraph('', '', ref_node)
        if item.badge is not None:
            bullet_list.append(attributetable_item('', item.badge, paragraph))
        else:
            bullet_list.append(attributetable_item('', paragraph))

    return attributetablecolumn('', header, bullet_list)


def setup(application):
    print('Initializing attribute table setup')
    application.add_directive('attributetable', PyAttributeTable)
    application.add_node(attributetable, html=(visit_attributetable_node, depart_attributetable_node))
    application.add_node(attributetablecolumn, html=(visit_attributetablecolumn_node, depart_attributetablecolumn_node))
    application.add_node(attributetabletitle, html=(visit_attributetabletitle_node, depart_attributetabletitle_node))
    application.add_node(attributetablebadge, html=(visit_attributetablebadge_node, depart_attributetablebadge_node))
    application.add_node(attributetable_item, html=(visit_attributetable_item_node, depart_attributetable_item_node))
    application.add_node(attributetableplaceholder)
    application.connect('doctree-resolved', process_attributetable)
