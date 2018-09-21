abadge
======

Generate status badges/shields of pure HTML+CSS.

.. image:: docs/abadge-discovered.png

Overview
--------

The ``Badge`` class in the module is used to generate status badges. It
supports various configuration options like font, background etc., and also
includes threshold support, which is useful for presenting job status, for
example.

Usage
-----

``Badge`` can be instantiated to generate many badges with the same format::

    from abadge import Badge
    
    success_badge = Badge(value_text_color='#11a')
    print(success_badge.to_html('build', 'passed'))
    print(success_badge.to_html('tests', 'ok'))

or for one-shot generation::

    print(Badge(label='tests', value='4/8').to_html())
    print(Badge().to_html(label='tests', value='4/8'))  # Same thing
    print(Badge.make_badge(tests, '4/8'))               # This too

The arguments to all of the methods are identical. The arguments to the
constructor will be stored in the instance as default values which can then
be overridden by the arguments to the ``to_html`` method. ``make_badge`` always
use the class default configuration (it is a class method).

Arguments
'''''''''

All three methods support the following arguments:

Optional arguments
..................

:*label*:
    text for the label (left) part. Can also be given as keyword argument
    ``label=<text>``

:*value*:
    text for the value (right) part. Can also be given as keyword argument
    ``value=<text>``

Keyword arguments
.................

:``border_radius``:
    how rounded the corners of the badge should be (CSS "``padding``")

:``font_family``: font to use in the badge (CSS "``font-family``")

:``font_size``: font size to use in the badge (CSS "``font-size``")

:``label``: the text in label part of the badge

:``label_background``:
    background color for the label (left) part (CSS "``background``")

:``label_text_color``:
    text color for the label (left) part (CSS "``color``")

:``label_text_shadow``:
    configuration for the text shadow (CSS "``text-shadow``")

:``link_decoration``:
    decoration for the link (CSS "``text-decoration``")

:``padding``:
    amount of space between the border and the text (CSS "``padding``")

:``thresholds``:
    dict with *label*-specific configuration options, so that multiple labels
    can be handled by the same class instance. See `Thresholds`_ below

:``url``: makes the badge link to the given URL

:``value``: the text in the value part of the badge

:``value_background``:
    background color for the value part (CSS "``background``"). This is also
    the final fallback if the value is neither found in ``thresholds`` nor in
    ``value_backgrounds``

:``value_backgrounds``:
    dict with *value* to ``value_background`` mappings. See `Thresholds`_
    below

:``value_text_color``: text color for the value part (CSS "``color``")

:``value_text_shadow``:
    configuration for the text shadow (CSS "``text-shadow``")

Thresholds
''''''''''

The ``thresholds`` argument is a dict with label as key and a configuration
dict as value. The dict supports the following keys:

:``order``:
    May be: ``auto``, ``float``, ``int``, ``str``, or ``strict``, with ``auto``
    being the default if ``order`` does not exist. ``float``, ``int`` and
    ``str`` forces level of that type (see below). ``auto`` uses ordering of
    type *float* or *int* if all *values* in ``colors`` are numbers type, with
    ``float`` taking precedence. If ``auto`` is set and at least one value is a
    string, or if ``strict`` is set, then an exact match is used for
    determining color, ie. no ordering

:``colors``:
    dict with *value* to *color* mapping

:``above``:
    Value is a color. if an ordering is requested, and the given value is above
    the highest value (key) in ``colors``, then this color is used

:``shade``:
    Whether to shade the color depending on distance between the thresholds.
    Each R, G, and B color is calculated based on the fraction of the distance
    of the value between the thresholds

Levels are handled by sorting the keys in the ``colors`` dict and comparing
the incoming value to each of the keys, starting with the key with the lowest
value, until the value is lower than or equal to the key::

    for k in sorted(thresholds['colors'].keys, key=<sort by type>):
        if value <= k:
            return thresholds['colors'][k]
    return thresholds['above']

Examples
--------

One instance can be configure to product different label types::

    build_badge = Badge(thresholds={
        'build': {
            'colors': {'SUCCESS': '#0f0',
                       'FAILURE': '#f00',
                       'UNSTABLE': '#ff0',
                       'ABORTED': '#f80', }},
        'KPI': {
            'order': 'str',
            'colors': {'A': '#0f4',
                       'B': '#f04',
                       'C': '#f84',
                       'D': '#ff4', }},
        'passrate': {
            'colors': {0.3: '#f00',
                       0.6: '#c40',
                       0.8: '#4c0', },
            'above': '#0f0', }})

    print(build_badge.to_html('build', 'UNSTABLE'))

    # Using a non-existing value will use the value_background color
    print(build_badge.to_html('build', 'SKIP'))
    print(build_badge.to_html('build', 'HOP', value_background='#ccc'))
    print(build_badge.to_html('passrate', 0.5))

.. image:: docs/example-build.png

If the color is not found in ``thresholds`` then the value will be looked
up in the ``value_backgrounds`` dict as a fallback::

    build_badge = Badge(thresholds={
        'build': {
            'colors': {'SUCCESS': '#0f0',
                       'FAILURE': '#f00',
                       'UNSTABLE': '#ff0',
                       'ABORTED': '#f80', }},
        'value_backgrounds': {'SUCCESS': '#0f4',
                              'FAILURE': '#f04',
                              'UNSTABLE': '#f84',
                              'ABORTED': '#ff4'}})
    print(build_badge.to_html('test', 'ABORTED'))

.. image:: docs/example-fallback.png

Shading does not produce color steps, but a shade between the colors in the
threshold. Shading only works for "float" and "int" types::

    build_badge = Badge(thresholds={
        'speed': {
            'shade': True,
            'colors': {0: '#0f0',
                       120: '#f00'},  # speed limit
            'above': '#f08'}}         # too fast!
    )
    print(build_badge.to_html('speed', 97))

    # Here is the rainbow
    build_badge = Badge(thresholds={
        'rainbow': {
            'shade': True,
            'colors': {0.0: '#ff0000',
                       1.0: '#ffff00',
                       2.0: '#00ff00',
                       3.0: '#00ffff',
                       4.0: '#0000ff',
                       5.0: '#8000ff'}}})

    for c in range(0, 11):
        print(build_badge.to_html('rainbow', c / 2.0))

.. image:: docs/example-shading.png
