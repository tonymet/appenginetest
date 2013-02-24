import traceback
import os
from google.appengine.api import urlfetch
from google.appengine.runtime import DeadlineExceededError
from google.appengine.api.labs import taskqueue
from model.Facebook import Facebook, FacebookApiError
from google.appengine.ext.webapp import template
from model.TaskModel import UserModel
import datetime
import Cookie
import logging
from uuid import uuid4
import json
from conf import facebook_conf
import urllib
import webapp2
import base64

class BaseHandler(webapp2.RequestHandler):
    facebook = None
    user = None
    csrf_protect = True
    csrf_token = None

    def initialize(self, request, response):
        """General initialization for every request"""
        super(BaseHandler, self).initialize(request, response)

        try:
            self.init_facebook()
            self.init_csrf()
            self.response.headers[u'P3P'] = u'CP=HONK'  # iframe cookies in IE
        except Exception, ex:
            self.log_exception(ex)
            raise

    def handle_exception(self, ex, debug_mode):
        """Invoked for unhandled exceptions by webapp"""
        self.log_exception(ex)
        self.render(u'error',
            trace=traceback.format_exc(), debug_mode=debug_mode)

    def log_exception(self, ex):
        """Internal logging handler to reduce some App Engine noise in errors"""
        msg = ((str(ex) or ex.__class__.__name__) +
                u': \n' + traceback.format_exc())
        if isinstance(ex, urlfetch.DownloadError) or \
           isinstance(ex, DeadlineExceededError) or \
           isinstance(ex, taskqueue.TransientError):
            logging.warn(msg)
        else:
            logging.error(msg)

    def set_cookie(self, name, value, expires=None):
        """Set a cookie"""
        if value is None:
            value = 'deleted'
            expires = datetime.timedelta(minutes=-50000)
        jar = Cookie.SimpleCookie()
        jar[name] = value
        jar[name]['path'] = u'/'
        if expires:
            if isinstance(expires, datetime.timedelta):
                expires = datetime.datetime.now() + expires
            if isinstance(expires, datetime.datetime):
                expires = expires.strftime('%a, %d %b %Y %H:%M:%S')
            jar[name]['expires'] = expires
        self.response.headers.add_header(*jar.output().split(u': ', 1))

    def render(self, name, **data):
        """Render a template"""
        if not data:
            data = {}
        data[u'js_conf'] = json.dumps({
            u'appId': facebook_conf.FACEBOOK_APP_ID,
            u'canvasName': facebook_conf.FACEBOOK_CANVAS_NAME,
            u'userIdOnServer': self.user.user_id if self.user else None,
        })
        data[u'logged_in_user'] = self.user
        data[u'message'] = self.get_message()
        data[u'csrf_token'] = self.csrf_token
        data[u'canvas_name'] = facebook_conf.FACEBOOK_CANVAS_NAME
        self.response.out.write( \
            template.render( \
                os.path.join( 'template', name + '.html'), 
                data)
        )

    def init_facebook(self):
        """Sets up the request specific Facebook and User instance"""
        facebook = Facebook()
        user = None

        if self.cookie_name() in self.request.cookies:
            try:
                facebook.load_signed_request(self.request.cookies.get(self.cookie_name()))
            except Exception as e:
                logging.error(str(e))

            if facebook.signed_request is None:
                raise Exception(u'ERROR: unable to parse signed request')
        else:
            #pass
            logging.error(u'no signed request cookie')

        # try to load or create a user object
        if facebook.user_id:
            user = UserModel.get_by_key_name(facebook.user_id)
            if user:
                # update stored access_token
                if facebook.access_token and \
                        facebook.access_token != user.access_token:
                    user.access_token = facebook.access_token
                    user.put()
                # refresh data if we failed in doing so after a realtime ping
                if user.dirty:
                    user.refresh_data()
                # restore stored access_token if necessary
                if not facebook.access_token:
                    facebook.access_token = user.access_token

            else:
            # if not user and facebook.access_token:
                try:
                    me = facebook.api(u'/me', {u'fields': u'picture,friends,name,first_name'})
                    user = UserModel(key_name=facebook.user_id,
                        user_id=facebook.user_id,
                        access_token=facebook.access_token,
                        name=me[u'name'],
                        email=me.get(u'email'),  # optional
                        picture=me[u'picture']['data']['url'],
                        friends=[user[u'id'] for user in me[u'friends'][u'data']])
                    user.put()
                except FacebookApiError as e:
                    logging.error("Error calling facebook" + str(e))
        else:
            logging.error("no user_id")

        self.facebook = facebook
        self.user = user

    def init_csrf(self):
        """Issue and handle CSRF token as necessary"""
        self.csrf_token = self.request.cookies.get(u'c')
        if not self.csrf_token:
            self.csrf_token = str(uuid4())[:8]
            self.set_cookie('c', self.csrf_token)
        if self.request.method == u'POST' and self.csrf_protect and \
                self.csrf_token != self.request.POST.get(u'_csrf_token'):
            raise Exception(u'Missing or invalid CSRF token.')

    def set_message(self, **obj):
        """Simple message support"""
        self.set_cookie('m', base64.b64encode(json.dumps(obj)) if obj else None)

    def get_message(self):
        """Get and clear the current message"""
        message = self.request.cookies.get(u'm')
        if message:
            self.set_message()  # clear the current cookie
            return json.loads(base64.b64decode(message))

    def cookie_name(self):
        return 'fbsr_%s' % facebook_conf.FACEBOOK_APP_ID

    def redirectToLogin(self):
        state = 'xxx'
        dialog_url = "https://www.facebook.com/dialog/oauth?" + urllib.urlencode({'client_id': facebook_conf.FACEBOOK_APP_ID,'redirect_uri': facebook_conf.EXTERNAL_HREF, 'state':state}) ;
        self.redirect(dialog_url)
