"""Test module for abadge."""

import unittest
from abadge import Badge


class BadgeTester(unittest.TestCase):
    """TestSuite for the abadge module."""

    default_config_template = (
        '<span style="background:#444;'
        'border-radius:4px 0px 0px 4px;color:white;'
        'font-family:DejaVu Sans, Verdana, sans;font-size:80%;'
        'padding:4px 8px 4px 8px;text-shadow:1px 1px black;">{label}</span>'
        '<span style="background:{value_background};'
        'border-radius:0px 4px 4px 0px;color:white;'
        'font-family:DejaVu Sans, Verdana, sans;font-size:80%;'
        'padding:4px 8px 4px 8px;text-shadow:1px 1px black;">{value}</span>'
    )

    def test_value_error_exception(self):
        with self.assertRaises(ValueError):
            Badge.make_badge('foo', 'bar', 'baz')

    def test_type_error_exception(self):
        with self.assertRaises(TypeError):
            Badge.make_badge('foo', 'bar', noexistent_keyword_argument='fake')

    def test_default_config(self):
        result = Badge.make_badge('foo', 'bar')
        self.assertEqual(
            self.default_config_template.format(label='foo',
                                                value='bar',
                                                value_background='#888',
                                                value_text_color='white'),
            result)

    def test_override_config(self):
        config = {
            'border_radius': '6px',
            'label': 'foo',
            'label_background': '#555',
            'label_text_color': 'black',
            'label_text_shadow': '2px 2px white',
            'font_family': 'mono',
            'font_size': '90%',
            'padding': '5px 5px 5px 9px',
            'url': 'foobar',
            'value': 'bar',
            'value_background': '#666',
            'value_text_color': 'blue',
            'value_text_shadow': '3px 3px red',
        }
        badge = Badge(**config)

        self.assertEqual(
            '<a href="foobar" style="text-decoration:none;">'
            '<span style="background:#555;border-radius:6px 0px 0px 6px;'
            'color:black;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:2px 2px white;">foo</span>'
            '<span style="background:#666;border-radius:0px 6px 6px 0px;'
            'color:blue;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:3px 3px red;">bar</span>'
            '</a>',
            badge.to_html())

        self.assertEqual(
            '<a href="foobar" style="text-decoration:golden;">'
            '<span style="background:overridden;border-radius:6px 0px 0px 6px;'
            'color:black;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:2px 2px white;">foo</span>'
            '<span style="background:#666;border-radius:0px 6px 6px 0px;'
            'color:blue;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:3px 3px red;">bar</span>'
            '</a>',
            badge.to_html(label_background='overridden',
                          link_decoration='golden'))

        badge = Badge('flip', 'flop', **config)

        self.assertEqual(
            '<a href="foobar" style="text-decoration:none;">'
            '<span style="background:#555;border-radius:6px 0px 0px 6px;'
            'color:black;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:2px 2px white;">flip</span>'
            '<span style="background:#666;border-radius:0px 6px 6px 0px;'
            'color:blue;font-family:mono;font-size:90%;'
            'padding:5px 5px 5px 9px;'
            'text-shadow:3px 3px red;">flop</span>'
            '</a>',
            badge.to_html())

    def test_backgrounds(self):
        badge = Badge(value_backgrounds={'a': 'ac', 'b': 'bc', 'c': 'cc'})
        result = badge.to_html('foo', 'a')
        self.assertEqual(
            self.default_config_template.format(label='foo',
                                                value='a',
                                                value_background='ac'),
            result)

        result = badge.to_html('bar', 'b')
        self.assertEqual(
            self.default_config_template.format(label='bar',
                                                value='b',
                                                value_background='bc'),
            result)

        result = badge.to_html('baz', 'c')
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='c',
                                                value_background='cc'),
            result)

    def test_single_thresholds(self):
        badge = Badge(thresholds={'foo': {'colors': {'a': 'ac'}},
                                  'bar': {'colors': {'b': 'bc'}}, },
                      value_backgrounds={'u': 'uc'})
        result = badge.to_html('foo', 'a')
        self.assertEqual(
            self.default_config_template.format(label='foo',
                                                value='a',
                                                value_background='ac'),
            result)

        result = badge.to_html('bar', 'b')
        self.assertEqual(
            self.default_config_template.format(label='bar',
                                                value='b',
                                                value_background='bc'),
            result)

        result = badge.to_html('baz', 'u')
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='u',
                                                value_background='uc'),
            result)

    def test_comparing_thresholds(self):
        badge = Badge(thresholds={'foo': {'colors': {'a': 'ac'},
                                          'order': 'str',
                                          'above': 'xc', },
                                  'bar': {'order': 'str',
                                          'colors': {'b': 'bc',
                                                     'd': 'dc', }},
                                  'baz': {'order': 'int',
                                          'colors': {1: '1c',
                                                     3: '3c', },
                                          'above': 'xc', },
                                  'boz': {'order': 'float',
                                          'colors': {1.1: '1.1c',
                                                     3.2: '3.2c', },
                                          'above': 'xc', },
                                  },
                      value_backgrounds={'u': 'uc'})
        # Strings
        result = badge.to_html('foo', 'a')
        self.assertEqual(
            self.default_config_template.format(label='foo',
                                                value='a',
                                                value_background='ac'),
            result)
        result = badge.to_html('foo', 'b')
        self.assertEqual(
            self.default_config_template.format(label='foo',
                                                value='b',
                                                value_background='xc'),
            result)

        result = badge.to_html('bar', 'a')
        self.assertEqual(
            self.default_config_template.format(label='bar',
                                                value='a',
                                                value_background='bc'),
            result)
        result = badge.to_html('bar', 'b')
        self.assertEqual(
            self.default_config_template.format(label='bar',
                                                value='b',
                                                value_background='bc'),
            result)
        result = badge.to_html('bar', 'u')
        self.assertEqual(
            self.default_config_template.format(label='bar',
                                                value='u',
                                                value_background='uc'),
            result)

        # Integers
        result = badge.to_html('baz', 0)
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='0',
                                                value_background='1c'),
            result)
        result = badge.to_html('baz', 1)
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='1',
                                                value_background='1c'),
            result)
        result = badge.to_html('baz', 2)
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='2',
                                                value_background='3c'),
            result)
        result = badge.to_html('baz', 4)
        self.assertEqual(
            self.default_config_template.format(label='baz',
                                                value='4',
                                                value_background='xc'),
            result)

        # Floats
        result = badge.to_html('boz', 0.5)
        self.assertEqual(
            self.default_config_template.format(label='boz',
                                                value='0.5',
                                                value_background='1.1c'),
            result)
        result = badge.to_html('boz', 1.01)
        self.assertEqual(
            self.default_config_template.format(label='boz',
                                                value='1.01',
                                                value_background='1.1c'),
            result)
        result = badge.to_html('boz', 1.11)
        self.assertEqual(
            self.default_config_template.format(label='boz',
                                                value='1.11',
                                                value_background='3.2c'),
            result)
        result = badge.to_html('boz', 4)
        self.assertEqual(
            self.default_config_template.format(label='boz',
                                                value='4',
                                                value_background='xc'),
            result)

    def test_link_target(self):
        badge = Badge.make_badge(url='foobar', link_target="_new")
        self.assertRegex(badge, '^<a href="foobar" target="_new" ')

        badge = Badge.make_badge(url='foobar', link_target="_blank")
        self.assertRegex(badge, '^<a href="foobar" target="_blank"'
                                ' rel="noopener noreferer" ')
