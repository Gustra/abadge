# abadge

Generate status badges/shields of pure HTML+CSS.

<span style="background:#444;border-radius:4px;font-family:DejaVu Sans, Verdana, sans;font-size:80%;padding:4px 8px 4px 8px;text-color:white;text-shadow:1px 1px black;"></span><span style="background:#2a2;border-radius:4px;font-family:DejaVu Sans, Verdana, sans;font-size:80%;padding:4px 8px 4px 8px;text-color:white;text-shadow:1px 1px black;"></span>

This module contains the `Badge` class which is used to generate status
badges in pure HTML+CSS.

## Usage

`Badge` can be instantiated to generate many badges with the same format:

    from abadge import Badge
    
    success_badge = Badge(value_text_color='#11a')
    print(success_badge.to_html('build', 'passed'))
    print(success_badge.to_html('tests', 'ok'))

or for one-shot generation:

    print(Badge(label='tests', value='4/8').to_html())
    print(Badge().to_html(label='tests', value='4/8'))  # Same thing
    print(Badge.make_badge(tests, '4/8'))               # This too

The arguments to all of the methods are identical. The arguments to the
constructor will be stored in the instance as default values which can then
be overridden by the arguments to the `to_html` method. `make_badge` always
use the class default configuration since it is a class method.

### Arguments

All three methods supports the following arguments:

#### Optional arguments

label
: text for the label (left) part. Can also be given as keyword argument `label=<text>`

value
: text for the value (right) part. Can also be given as keyword argument `value=<text>`

#### Keyword arguments

border_radius
: how rounded the corners of the badge should be (CSS "padding")

label
: the text in label part of the badge

label_background
: background color for the label (left) part (CSS "background")

label_text_color
: text color for the label (left) part (CSS "text-color")

label_text_shadow
: configuration for the text shadow (CSS "text-shadow")

font_family
: font to use in the badge (CSS "font-family")

padding
: amount of space between the border and the text (CSS "padding")

thresholds
: dict with value to `value_background` mappings. See Thresholds below

value
: the text in the value part of the badge

value_background
: background color for the label (left) part (CSS "background")

value_text_color
: text color for the label (left) part (CSS "text-color")

value_text_shadow
: configuration for the text shadow (CSS "text-shadow")

### Thresholds

The `thresholds` argument is a dict with simple value to background color mapping:

    build_badge = Badge(thresholds={'SUCCESS': '#0f0',
                                    'FAILURE': '#f00',
                                    'UNSTABLE': '#ff0',
                                    'ABORTED': '#f80',})
    print(build_badge('build', job.get_status()))
