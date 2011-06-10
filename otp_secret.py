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

class OtpSecret(db.Model):

    id = db.IntegerProperty(required=True)
    secret = db.StringProperty(required=True)
    moving_factor = db.IntegerProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
    owner = db.UserProperty(required=True)

