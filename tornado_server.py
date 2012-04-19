#!/usr/bin/env python

import json
import os

from tornado.escape import utf8
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line, parse_config_file
from tornado.web import RequestHandler, Application, asynchronous, authenticated, HTTPError

from async_dropbox import DropboxMixin

define('port', default=8888)
define('flagfile', default='config.flags')
define('debug', default=False)
define('cookie_secret', default="3f8c0458deffeb471fc4142c1c0ad232")

# These don't have defaults; see README for details.
define('dropbox_consumer_key')
define('dropbox_consumer_secret')

class BaseHandler(RequestHandler):
    def get_current_user(self):
        if self.get_secure_cookie("user"):
            return json.loads(self.get_secure_cookie("user"))
        else:
            return None

    def get_access_token(self):
        # json turns this into unicode strings, but we need bytes for oauth
        # signatures.
        return dict((utf8(k), utf8(v)) for (k, v) in self.current_user["access_token"].iteritems())

class RootHandler(BaseHandler, DropboxMixin):
    @authenticated
    #@asynchronous
    def get(self):
        self.write("Username: %s<br>Password: %s<br>Token: %s"
            % ("user", "12345", str(self.get_access_token())))
        #self.dropbox_request('api', '/1/metadata/sandbox/', self.on_metadata,
        #                     self.get_access_token(),
        #                     list="true")

    #def on_metadata(self, response):
    #    response.rethrow()
    #    metadata = json.load(response.buffer)
    #    self.render("index.html", metadata=metadata)

def tornado_main():
    parse_command_line()
    parse_config_file(options.flagfile)

    settings = dict(
        login_url='/login',
        debug=options.debug,
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),

        cookie_secret=options.cookie_secret,
        dropbox_consumer_key=options.dropbox_consumer_key,
        dropbox_consumer_secret=options.dropbox_consumer_secret,
        )
    app = Application([
            ('/', RootHandler),
            ], **settings)
    app.listen(options.port)
    IOLoop.instance().start()

if __name__ == '__main__':
    tornado_main()
