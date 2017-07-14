# coding=utf8
"""
Wolfram|Alpha module for Sopel IRC bot framework
Forked from code by Max Gurela (@maxpowa):
https://github.com/maxpowa/inumuta-modules/blob/e0b195c4f1e1b788fa77ec2144d39c4748886a6a/wolfram.py
Updated and packaged for PyPI by dgw (@dgw)
"""

from __future__ import unicode_literals
from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import commands, example
from sopel import web
import wolframalpha


class WolframSection(StaticSection):
    app_id = ValidatedAttribute('app_id', default=None)
    max_public = ValidatedAttribute('max_public', default=5)
    units = ChoiceAttribute('units', choices=['metric', 'nonmetric'], default='metric')


def configure(config):
    config.define_section('wolfram', WolframSection, validate=False)
    config.wolfram.configure_setting('app_id', 'Application ID')
    config.wolfram.configure_setting('max_public', 'Maximum lines before sending answer in NOTICE')


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

    lines = (msg or wa_query(bot.config.wolfram.app_id, trigger.group(2), bot.config.wolfram.units)).splitlines()

    if len(lines) <= bot.config.wolfram.max_public:
        for line in lines:
            bot.say('[W|A] {}'.format(line))
    else:
        for line in lines:
            bot.notice('[W|A] {}'.format(line), trigger.nick)


def wa_query(app_id, query, units='metric'):
    if not app_id:
        return 'Wolfram|Alpha API app ID not provided.'
    client = wolframalpha.Client(app_id)
    query = query.encode('utf-8').strip()
    params = (
        ('format', 'plaintext'),
        ('units', units),
    )

    try:  # Remove this mess for the next bump after 0.4
        try:  # wolframalpha 3.x supports extra stuff
            result = client.query(input=query, params=params)  # This is the only necessary line post-0.4
        except TypeError:  # fall back to query-only for 2.x
            try:
                result = client.query(query)
            except:
                raise  # send any exceptions to the outer level
        except:
            raise  # ditto; the 0.4 mess ends here
    except AssertionError:
        return 'Temporary API issue. Try again in a moment.'
    except Exception as e:
        return 'Query failed: {} ({})'.format(type(e).__name__, e.message or 'Unknown error, try again!')

    num_results = 0
    try:  # try wolframalpha 3.x way
        num_results = int(result['@numpods'])
    except TypeError:  # fall back to wolframalpha 2.x way
        num_results = len(result.pods)
    finally:
        if num_results == 0:
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
        return 'Unhandled {}; please report this query ("{}") at https://dgw.me/wabug'.format(type(e).__name__, query)

    try:
        input, output = texts[0], texts[1]
    except IndexError:
        return 'No text-representable result found; see http://wolframalpha.com/input/?i={}'.format(web.quote(query))

    if not output:
        return input
    return '{} = {}'.format(input, output)
