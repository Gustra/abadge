abadge
======

Generate status badges/shields of pure HTML+CSS.

.. image:: abadge-discovered.png

Overview
--------

The ``Badge`` class in the module is used to generate status badges. It
supports various configuration options like font, background etc., and also
includes rudimentary threshold support, which is useful for presenting job
status, for example.

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
    dict with *value* to ``value_background`` mappings. See `Thresholds`_
    below

:``url``: makes the badge link to the given URL

:``value``: the text in the value part of the badge

:``value_background``:
    background color for the value part (CSS "``background``")

:``value_text_color``: text color for the value part (CSS "``color``")

:``value_text_shadow``:
    configuration for the text shadow (CSS "``text-shadow``")

Thresholds
''''''''''

The ``thresholds`` argument is a dict with simple value to background color
mapping::

    build_badge = Badge(thresholds={'SUCCESS': '#0f0',
                                    'FAILURE': '#f00',
                                    'UNSTABLE': '#ff0',
                                    'ABORTED': '#f80',})
    print(build_badge('build', job.get_status()))
    # Using a non-existing value will use the value_background color
    print(build_badge('build', 'SKIP'))
    print(build_badge('build', 'HOP', value_background='#888'))

