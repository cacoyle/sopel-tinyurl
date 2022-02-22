#!env/bin/python

from sopel.config.types import StaticSection, ChoiceAttribute, ValidatedAttribute
from sopel.module import commands, example
from sopel import web

import sopel.module

import re
import requests

URL_RE = r'^.*(https?://[^\s]*).*$'

class TinyurlSection(StaticSection):
		api_token = ValidatedAttribute('api_token', default=None)
		api_url  = ValidatedAttribute('api_url', default='https://api.tinyurl.com/create')
		max_url_length = ValidatedAttribute('max_url_length', default=64)


def configure(config):
		config.tinyurl.configure_setting('api_token', 'tinyurl api token')
		config.tinyurl.configure_setting('api_url', 'tinyurl api url')
		config.tinyurl.configure_setting('max_url_length', 'max url length before being converted to tinyurl')


def setup(bot):
		bot.config.define_section('tinyurl', TinyurlSection)


def check(bot, trigger):
		msg = None
		if not bot.config.tinyurl.api_token:
				msg = 'Tinyurl api token not configured.'


def create_tinyurl(api_endpoint, token, url):
	result = requests.post(
		api_endpoint,
		headers={
			'accept': 'application/json',
			'Authorization': f"Bearer {token}",
			'Content-Type': 'application/json',
		},
		json={
			'url': url
		}
	)

	return result.json()['data']['tiny_url']


@sopel.plugin.rule(URL_RE)
def shorten_url(bot, trigger)
	shamee = trigger.nick  # Maybe use later.

	re_res = re.match(URL_RE, trigger)

	if re_res:
		if len(re_res.groups()[0]) >= bot.config.tinyurl.max_url_length:
			tiny_result = create_tinyurl(
				bot.config.tinyurl.api_url,
				bot.config.tinyurl.api_token,
				re_res.groups()[0]
			)

			bot.say(tiny_result)
