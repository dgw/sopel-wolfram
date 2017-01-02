# coding=utf8
"""
Wolfram|Alpha module for Sopel IRC bot framework
Forked from code by Max Gurela (@maxpowa):
https://github.com/maxpowa/inumuta-modules/blob/e0b195c4f1e1b788fa77ec2144d39c4748886a6a/wolfram.py
Updated and packaged for PyPI by dgw (@dgw)
"""

from __future__ import unicode_literals
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example
from sopel import web
import wolframalpha


class WolframSection(StaticSection):
    app_id = ValidatedAttribute('app_id', default=None)


def configure(config):
    config.define_section('wolfram', WolframSection, validate=False)
    config.wolfram.configure_setting('app_id', 'Application ID')


def setup(bot):
    bot.config.define_section('wolfram', WolframSection)


@commands('wa', 'wolfram')
@example('.wa 2+2', '[W|A] 2+2 = 4')
@example('.wa python language release date', '[W|A] Python | date introduced = 1991')
def wa_command(bot, trigger):
    msg = None
    if not trigger.group(2):
        msg = 'You must provide a query.'
    if not bot.config.wolfram.app_id:
        msg = 'Wolfram|Alpha API app ID not configured.'

    lines = (msg or wa_query(bot.config.wolfram.app_id, trigger.group(2))).splitlines()

    if len(lines) <= 3:
        for line in lines:
            bot.say('[W|A] {}'.format(line))
    else:
        for line in lines:
            bot.notice('[W|A] {}'.format(line), trigger.nick)


def wa_query(app_id, query):
    if not app_id:
        return 'Wolfram|Alpha API app ID not provided.'
    client = wolframalpha.Client(app_id)
    query = query.encode('utf-8').strip()

    try:
        result = client.query(query)
    except Exception as e:
        return 'An error occurred: {}'.format(e.message or 'Unknown error, try again!')

    if len(result.pods) >= 2:
        try:
            input = result.pods[0].text
            output = result.pods[1].text
        except (IndexError, KeyError):
            pass
        else:
            return '{} = {}'.format(input, output)

    if len(result.pods) > 0:
        return 'No text-representable result found, see http://wolframalpha.com/input/?i={}'.format(web.quote(query))

    return 'No results found.'
