"""
Wolfram|Alpha plugin for Sopel IRC bot framework

Forked from code by Max Gurela (@maxpowa):
https://github.com/maxpowa/inumuta-modules/blob/e0b195c4f1e1b788fa77ec2144d39c4748886a6a/wolfram.py
Updated and packaged for PyPI by dgw (@dgw)
"""
from __future__ import annotations

import wolframalpha

from sopel.config.types import (
    ChoiceAttribute,
    SecretAttribute,
    StaticSection,
    ValidatedAttribute,
)
from sopel.plugin import commands, example, output_prefix
from sopel.tools import web


UNITS = ('metric', 'nonmetric')


class WolframSection(StaticSection):
    app_id = SecretAttribute('app_id', default=None)
    max_public = ValidatedAttribute('max_public', parse=int, default=5)
    units = ChoiceAttribute('units', choices=UNITS, default=UNITS[0])


def configure(config):
    config.define_section('wolfram', WolframSection, validate=False)
    config.wolfram.configure_setting('app_id', 'Wolfram|Alpha App ID:')
    config.wolfram.configure_setting('max_public', 'Maximum lines before sending answer in NOTICE:')
    config.wolfram.configure_setting(
        'units',
        'Unit system to use in output ({}):'.format(', '.join(UNITS)),
    )


def setup(bot):
    bot.config.define_section('wolfram', WolframSection)


@commands('wa', 'wolfram')
@example('.wa 2+2', '2 + 2 = 4')
@example('.wa python language release date', 'Python | date introduced = 1991')
@output_prefix('[W|A] ')
def wa_command(bot, trigger):
    msg = None
    if not trigger.group(2):
        msg = 'You must provide a query.'
    if not bot.config.wolfram.app_id:
        msg = 'Wolfram|Alpha API app ID not configured.'

    lines = (msg or wa_query(bot.config.wolfram.app_id, trigger.group(2), bot.config.wolfram.units)).splitlines()

    if len(lines) <= bot.config.wolfram.max_public:
        for line in lines:
            bot.say(line)
    else:
        for line in lines:
            bot.notice(line, trigger.nick)


def wa_query(app_id, query, units='metric'):
    if not app_id:
        return 'Wolfram|Alpha API app ID not provided.'

    client = wolframalpha.Client(app_id)
    query = query.strip()
    params = (
        ('format', 'plaintext'),
        ('units', units),
    )

    try:
        result = client.query(input=query, params=params)
    except AssertionError:
        return 'Temporary API issue. Try again in a moment.'
    except Exception as e:
        return 'Query failed: {} ({})'.format(type(e).__name__, str(e) or 'Unknown error, try again!')

    if int(result['@numpods']) == 0:
        return 'No results found.'

    texts = []
    try:
        for pod in result.pods:
            try:
                texts.append(pod.text)
            except AttributeError:
                pass  # pod with no text; skip it
            except Exception:
                raise  # raise unexpected exceptions to outer try for bug reports
            if len(texts) >= 2:
                break  # len() is O(1); this cheaply avoids copying more strings than needed
    except Exception as e:
        return 'Unhandled {}; please report this query ("{}") at https://git.io/wabug'.format(type(e).__name__, query)

    try:
        input, output = texts[0], texts[1]
    except IndexError:
        return 'No text-representable result found; see https://wolframalpha.com/input/?i={}'.format(web.quote(query))

    if not output:
        return input
    return '{} = {}'.format(input, output)
