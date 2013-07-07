#!/usr/bin/env python
#
# Copyright 2013 Adam Gschwender
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import hashlib
import hmac
import re
import urllib
import urlparse

def derive_signature(key, qs):
    """Derives the signature from the supplied query string using the key."""
    return hmac.new(key, qs, hashlib.sha1).hexdigest()

def sign(key, qs):
    """Signs the query string using the key."""
    sig = derive_signature(key, qs)
    return "%s&%s" % (qs, urllib.urlencode([("sig", sig)]))

def verify_signature(key, qs):
    """Verifies that the signature in the query string is correct."""
    unsigned_qs = re.sub(r'&?sig=[^&]*', '', qs)
    sig = derive_signature(key, unsigned_qs)
    return urlparse.parse_qs(qs).get("sig", [None])[0] == sig


def main():
    import sys
    import tornado.options
    from tornado.options import define, options, parse_command_line
    define("key", help="the signing key", type=str)
    args = parse_command_line()
    if not options.key:
        tornado.options.print_help()
        sys.exit()
    for i, arg in enumerate(args):
        if i > 0:
            print "=" * 78
        print "Query String: %s" % arg
        print "Signature: %s" % derive_signature(options.key, arg)
        print "Signed Query String: %s" % sign(options.key, arg)

if __name__ == "__main__":
    main()
