"""Test module for abadge."""

import unittest
from abadge import Badge


class BadgeTester(unittest.TestCase):
    """TestSuite for the abadge module."""

    default_config_template = ('<span style="background:#444;border-radius:4px;'
                               'font-family:DejaVu Sans, Verdana, sans;font-size:80%;padding:4px 8px 4px 8px;'
                               'text-color:white;text-shadow:1px 1px black;">{label}</span>'
                               '<span style="background:{value_background};border-radius:4px;'
                               'font-family:DejaVu Sans, Verdana, sans;font-size:80%;padding:4px 8px 4px 8px;'
                               'text-color:white;text-shadow:1px 1px black;">{value}</span>')

    def test_value_error_exception(self):
        with self.assertRaises(ValueError):
            Badge.make_badge('foo', 'bar', 'baz')

    def test_type_error_exception(self):
        with self.assertRaises(TypeError):
            Badge.make_badge('foo', 'bar', noexistent_keyword_argument='fake')

    def test_default_config(self):
        result = Badge.make_badge('foo', 'bar')
        self.assertEqual(self.default_config_template.format(label='foo',
                                                             value='bar',
                                                             value_background='#444',
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
            'value': 'bar',
            'value_background': '#666',
            'value_text_color': 'blue',
            'value_text_shadow': '3px 3px red',
        }
        badge = Badge(**config)

        self.assertEqual('<span style="background:#555;border-radius:6px;'
                         'font-family:mono;font-size:90%;padding:5px 5px 5px 9px;'
                         'text-color:black;text-shadow:2px 2px white;">foo</span>'
                         '<span style="background:#666;border-radius:6px;'
                         'font-family:mono;font-size:90%;padding:5px 5px 5px 9px;'
                         'text-color:blue;text-shadow:3px 3px red;">bar</span>',
                         badge.to_html())

        self.assertEqual('<span style="background:overridden;border-radius:6px;'
                         'font-family:mono;font-size:90%;padding:5px 5px 5px 9px;'
                         'text-color:black;text-shadow:2px 2px white;">foo</span>'
                         '<span style="background:#666;border-radius:6px;'
                         'font-family:mono;font-size:90%;padding:5px 5px 5px 9px;'
                         'text-color:blue;text-shadow:3px 3px red;">bar</span>',
                         badge.to_html(label_background='overridden'))

    def test_levels(self):
        badge = Badge(thresholds={'a': 'ac', 'b': 'bc', 'c': 'cc'})
        result = badge.to_html('foo', 'a')
        self.assertEqual(self.default_config_template.format(label='foo',
                                                             value='a',
                                                             value_background='ac'),
                         result)

        result = badge.to_html('bar', 'b')
        self.assertEqual(self.default_config_template.format(label='bar',
                                                             value='b',
                                                             value_background='bc'),
                         result)

        result = badge.to_html('baz', 'c')
        self.assertEqual(self.default_config_template.format(label='baz',
                                                             value='c',
                                                             value_background='cc'),
                         result)
