Sopel Wolfram\|Alpha module
===========================

Wolfram\|Alpha module for Sopel IRC bot framework

Configuration
-------------

The Wolfram\|Alpha API requires a key to be added in the bot’s config.
Sign up for API access at http://developer.wolframalpha.com/portal/apisignup.html and add the App ID to Sopel’s configuration file:

::

    [wolfram]
    app_id = yourappidgoeshere

Usage
-----

::

    <User> .wa 2+2
    <Sopel> Result: 4
