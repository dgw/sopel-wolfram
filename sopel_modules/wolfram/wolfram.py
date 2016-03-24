# coding=utf8
"""
Wolfram|Alpha module for Sopel IRC framework
Original code copyright 2016 Max Gurela (@maxpowa), sourced from
https://github.com/maxpowa/inumuta-modules/blob/e0b195c4f1e1b788fa77ec2144d39c4748886a6a/wolfram.py
Packaged for PyPI by dgw (@dgw)
"""

from __future__ import unicode_literals
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands
from sopel import web
import wolframalpha
import json

output_ids = ['DecimalApproximation', 'Result', 'ExactResult']


class WolframSection(StaticSection):
    app_id = ValidatedAttribute('app_id', default=None)


def configure(config):
    config.define_section('wolfram', WolframSection, validate=False)
    config.wolfram.configure_setting('app_id', 'Application ID')


def setup(bot):
    bot.config.define_section('wolfram', WolframSection)


@commands('wa', 'wolfram')
def wa_query(bot, trigger):
    if not trigger.group(2):
        return bot.say('[Wolfram] You must provide a query')
    elif not bot.config.wolfram.app_id:
        return bot.say('[Wolfram] A Wolfram app ID must be configured for this module to function.')
    client = wolframalpha.Client(bot.config.wolfram.app_id)

    try:
        result = client.query(trigger.group(2))
    except Exception as e:
        return bot.say('[Wolfram] An error occurred ({})'.format(e.message))

    for pod in result.pods:
        if pod.id not in output_ids:
            continue
        return bot.say('{}: {}'.format(pod.title, pod.text))

    if len(result.pods) > 0:
        return bot.say('[Wolfram] No text-representable result found, see http://wolframalpha.com/input/?i={}'.format(web.quote(trigger.group(2))))

    return bot.say('[Wolfram] No results found.')
