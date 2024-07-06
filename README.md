# sopel-wolfram

Wolfram|Alpha plugin for the Sopel IRC bot framework

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-wolfram
```

### Requirements

* Sopel 8.x
* wolframalpha 5.x

You will also need a Wolfram|Alpha App ID; see details below in the
"Configuring" section.


## Configuring

The easiest way to configure `sopel-wolfram` is via Sopel's
configuration wizard—simply run `sopel-plugins configure wolfram`
and enter the values for which it prompts you.

However, you can manually add the following section to your Sopel bot's
configuration file if desired:

```ini
[wolfram]
app_id = yourappidgoeshere
```

The `app_id` setting is required, and you will need to get your own App ID from
Wolfram|Alpha at https://developer.wolframalpha.com/

Optional settings:

* `max_public`: the number of lines over which results will be sent in NOTICE
  instead of to the channel (default: 5)
* `units`: measurement system displayed in results, either `metric` (the
  default) or `nonmetric`


## Example usage

```
<User> .wa 2+2
<Sopel> [W|A] 2+2 = 4

<User> .wa python language release date
<Sopel> [W|A] Python | date introduced = 1991

<User> .wa airspeed velocity of an unladen swallow
<Sopel> [W|A] estimated average cruising airspeed of an unladen European
        swallow = 25 mph  (miles per hour)(asked, but not answered, about a
        general swallow in the 1975 film Monty Python and the Holy Grail)
```
