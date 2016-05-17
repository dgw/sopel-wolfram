Sopel Wolfram\|Alpha module
===========================

Wolfram\|Alpha module for Sopel IRC bot framework

Installation
------------

This package's full name is ``sopel-modules.wolfram`` and it is listed on PyPI under
that identifier.

The only supported installation method is via ``pip``::

    pip install sopel-modules.wolfram

Use ``pip3`` as appropriate for your Python environment.

Development versions can be installed from GitHub via ``pip`` also::

    pip install git+https://github.com/dgw/sopel-wolfram.git@master

Note that ``pip`` does not keep track of packages obtained from sources outside of
PyPI, so ``pip install --upgrade sopel-modules.wolfram`` will not work for GitHub
installations. Instead, to upgrade to the latest code, do::

    pip install --upgrade git+https://github.com/dgw/sopel-wolfram.git@master

Configuration
-------------

The Wolfram\|Alpha API requires a key to be added in the bot’s config. Sign up for API
access at http://developer.wolframalpha.com/portal/apisignup.html and add the App ID
to Sopel’s configuration file:

::

    [wolfram]
    app_id = yourappidgoeshere

Usage
-----

::

    <User> .wa 2+2
    <Sopel> [W|A] 2+2 = 4

    <User> .wa python language release date
    <Sopel> [W|A] Python | date introduced = 1991

    <User> .wa airspeed velocity of an unladen swallow
    <Sopel> [W|A] estimated average cruising airspeed of an unladen European swallow
            = 25 mph  (miles per hour)(asked, but not answered, about a general
            swallow in the 1975 film Monty Python and the Holy Grail)

A Note About Reloading
----------------------

In versions of sopel up to 6.3.1 (the last tested version), reloading a third-party module
installed from pip, such as wolfram, results in duplicated output. This is `a known issue in
sopel <https://github.com/sopel-irc/sopel/issues/1056>`_ and is being worked on.

**Workaround:** After updating sopel-wolfram through pip, restart the bot at your earliest
convenience to enable the latest code.

Support
-------

Help with installing or configuring the module is available by pinging either
``dgw`` or ``maxpowa`` in ``#sopel`` on freenode. ``dgw`` is also available in
``#Kaede`` on Rizon.

Bugs and feature requests can be `submitted <https://github.com/dgw/sopel-wolfram/issues/new>`_
to the GitHub issue tracker, preferably after first bringing them up on IRC.
