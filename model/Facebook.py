import base64
import hmac
import hashlib
import time
import json
from conf import facebook_conf
from google.appengine.api import urlfetch
import urllib
import urlparse
import logging
import pprint

class FacebookApiError(Exception):
	def __init__(self, result):
		self.result = result
	def __str__(self):
		return pprint.pformat(self.result) 	


class Facebook(object):
	"""Wraps the Facebook specific logic"""
	def __init__(self, app_id=facebook_conf.FACEBOOK_APP_ID,
			app_secret=facebook_conf.FACEBOOK_APP_SECRET):
		self.app_id = app_id
		self.app_secret = app_secret
		self.user_id = None
		self.access_token = None
		self.access_token_expires = None
		self.signed_request = {}

	def api(self, path, params=None, method=u'GET', domain=u'graph' ):
		"""Make API calls"""
		if not params:
			params = {}
		params[u'method'] = method
		if u'access_token' not in params and self.access_token:
			params[u'access_token'] = self.access_token
		result = json.loads(urlfetch.fetch(
			url=u'https://' + domain + u'.facebook.com' + path,
			payload=urllib.urlencode(params),
			method=urlfetch.POST,
			headers={
				u'Content-Type': u'application/x-www-form-urlencoded'})
			.content)
		if isinstance(result, dict) and u'error' in result:
			raise FacebookApiError(result)
		return result

	def load_signed_request(self, signed_request):
		"""Load the user state from a signed_request value"""
		sig, payload = signed_request.split(u'.', 1)
		sig = self.base64_url_decode(sig)
		data = json.loads(self.base64_url_decode(payload))

		logging.debug("signed_request: "  + str(data))
		expected_sig = hmac.new( self.app_secret, msg=payload, digestmod=hashlib.sha256).digest()

		oauth_token = self.auth_token_from_code(data.get('code'))
		if oauth_token is not None:
			data['oauth_token'] =  oauth_token

		if not data.get(u'oauth_token'):
			logging.error("missing oauth_token")
			return
		# allow the signed_request to function for upto 1 day
		if sig == expected_sig and data[u'issued_at'] > (time.time() - 86400):
			self.signed_request = data
			self.user_id = data.get(u'user_id')
			self.access_token = data.get(u'oauth_token')

	@property
	def user_cookie(self):
		"""Generate a signed_request value based on current state"""
		if not self.user_id:
			return
		payload = self.base64_url_encode(json.dumps({
			u'user_id': self.user_id,
			u'issued_at': str(int(time.time())),
		}))
		sig = self.base64_url_encode(hmac.new(
			self.app_secret, msg=payload, digestmod=hashlib.sha256).digest())
		return sig + '.' + payload

	@staticmethod
	def base64_url_decode(data):
		data = data.encode(u'ascii')
		data += '=' * (4 - (len(data) % 4))
		return base64.urlsafe_b64decode(data)

	@staticmethod
	def base64_url_encode(data):
		return base64.urlsafe_b64encode(data).rstrip('=')

	def auth_token_from_code(self,code):
		path = '/oauth/access_token'
		params = {
			'client_id': facebook_conf.FACEBOOK_APP_ID,
			'client_secret': facebook_conf.FACEBOOK_APP_SECRET,
			#'redirect_uri' : facebook_conf.EXTERNAL_HREF,
			'redirect_uri' : '',
			'code' : code
		}
		result = urlfetch.fetch(
			url=u'https://' + 'graph' + u'.facebook.com' + path,
			payload=urllib.urlencode(params),
			method=urlfetch.POST,
			headers={
				u'Content-Type': u'application/x-www-form-urlencoded'})
		if(result.status_code != 200):
			logging.debug("content: "  + result.content)
			logging.error("Error fetching access_token: " + str(result.status_code))
			return None
		else:
			data = urlparse.parse_qs(str(result.content))
			if data and 'access_token' in data and 'expires' in data:
				logging.debug(pprint.pformat(data));
				self.access_token = data['access_token'][0]
				self.access_token_expires = int(int(data['expires'][0]) + time.time())
				return self.access_token
			else:
				return none

	def get_user_info(self, code):
		me = facebook.api(u'/me', {u'fields': u'picture,friends'})
