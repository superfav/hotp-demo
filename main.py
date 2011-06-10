#!/usr/bin/python
# -*- coding: utf-8 -*-

#    This file is part of hotp-demo.
# 
#    hotp-demo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    hotp-demo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

from otp_secret import OtpSecret

import hotp
import os


class CreatePage(webapp.RequestHandler):

    def get(self):
        template_values = \
            {'logout_url': users.create_logout_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/create.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        id = self.request.get('id')
        secret = self.request.get('secret')
        otp_secret = OtpSecret(id=int(id), secret=secret,
                               moving_factor=0,
                               owner=users.get_current_user())
        otp_secret.put()
        self.redirect('/list')


class DeletePage(webapp.RequestHandler):

    def get(self):
        OtpSecret.get(db.Key(self.request.get('key'))).delete()
        self.redirect('/list')


class ListPage(webapp.RequestHandler):

    def get(self):
        template_values = {'secrets': OtpSecret.all().filter('owner',
                           users.get_current_user()).order('id'),
                           'logout_url': users.create_logout_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/list.html')
        self.response.out.write(template.render(path, template_values))


class VerifyPage(webapp.RequestHandler):

    def get(self):
        template_values = \
            {'logout_url': users.create_logout_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/verify.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        request = self.request
        status = '<span style="color: red">wrong password</span>'
        password = request.get('password')
        if request.get('id') and password:
            id = int(request.get('id'))
            secrets = OtpSecret.all().filter('owner',
                    users.get_current_user()).filter('id', id)
            if secrets:
                for secret in secrets:
                    for loop in range(0, 10):
                        try:
                            actual = secret.moving_factor + loop
                            genpin = hotp.hotp(secret.secret, actual)
                        except Exception, err:
                            break
                        if genpin == password:
                            status = 'OK'
                            secret.moving_factor = actual + 1
                            secret.put()
                            break
        template_values = {'status': status,
                           'logout_url': users.create_logout_url(self.request.uri)}
        path = os.path.join(os.path.dirname(__file__),
                            'templates/verify.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/list', ListPage),
            ('/create', CreatePage), ('/delete', DeletePage), ('/verify'
            , VerifyPage)], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
