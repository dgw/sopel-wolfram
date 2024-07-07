Sopel Wolfram\|Alpha plugin
===========================

Wolfram\|Alpha plugin for Sopel IRC bot framework

**Important: This package is no longer updated.** Please install `sopel-wolfram
<https://pypi.org/project/sopel-wolfram/>`_ for use with Sopel 8.0 and higher.


Requirements
------------

* Sopel 7.x
* wolframalpha 3.x


Installation
------------

This package's full name is ``sopel-modules.wolfram`` and it is `listed on PyPI
<https://pypi.python.org/pypi/sopel-modules.wolfram>`_ under that identifier.

The only supported installation method is via ``pip``::

    pip install sopel-modules.wolfram

Use ``pip3`` as appropriate for your Python environment.

Development versions can be installed from GitHub via ``pip`` also::

    pip install git+https://github.com/dgw/sopel-wolfram.git@master

Note that ``pip`` does not keep track of packages obtained from sources outside
of PyPI, so ``pip install --upgrade sopel-modules.wolfram`` will not work for
GitHub installations. Instead, to upgrade to the latest code, do::

    pip install --upgrade git+https://github.com/dgw/sopel-wolfram.git@master


Configuration
-------------

Required
::::::::

The Wolfram\|Alpha API requires a key to be added in the bot’s config. Click
the "Get an AppID" button at https://developer.wolframalpha.com/portal/myapps/
and add your new AppID to Sopel’s configuration file:

::

    [wolfram]
    app_id = yourappidgoeshere

Optional
::::::::

* ``max_public``: the number of lines over which results will be sent in NOTICE
  instead of to the channel (default: 10)
* ``units``: measurement system displayed in results, either ``metric`` (the
  default) or ``nonmetric``


Usage
-----

::

    <User> .wa 2+2
    <Sopel> [W|A] 2+2 = 4

    <User> .wa python language release date
    <Sopel> [W|A] Python | date introduced = 1991

    <User> .wa airspeed velocity of an unladen swallow
    <Sopel> [W|A] estimated average cruising airspeed of an unladen European
            swallow = 25 mph  (miles per hour)(asked, but not answered, about a
            general swallow in the 1975 film Monty Python and the Holy Grail)


A Note About Reloading
----------------------

Due to Python limitations, reloading a "packaged" Sopel plugin such as this
one, might not actually reload all of the code. After updating sopel-wolfram,
please restart the bot at your earliest convenience, rather than using Sopel's
``.reload`` function. The last tested version was: Sopel 7.0.0


Support
-------

Help with installing or configuring the module is available by pinging either
``dgw`` or ``maxpowa`` in ``#sopel`` on freenode. ``dgw`` is also available in
``#Kaede`` on Rizon.

Bugs and feature requests can be `submitted <https://github.com/dgw/sopel-wolfram/issues/new>`_
to the GitHub issue tracker, preferably after first bringing them up on IRC.
