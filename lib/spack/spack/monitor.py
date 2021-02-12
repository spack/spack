# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Interact with a Spack Monitor Service. Derived from
https://github.com/spack/spack-monitor/blob/main/script/spackmoncli.py
"""

import base64
import json
import logging
import os
import re
import sys

from urllib.request import Request, urlopen
from urllib.error import URLError

import llnl.util.tty as tty
from copy import deepcopy


def get_client(host, prefix="ms1", disable_auth=False, allow_fail=False):
    """a common function to get a client for a particular host and prefix.
    If the client is not running, we exit early, unless allow_fail is set
    to true, indicating that we should continue the build even if the
    server is not present.
    """
    cli = SpackMonitorClient(host=host, prefix=prefix, allow_fail=allow_fail)

    # If we don't disable auth, environment credentials are required
    if not disable_auth:
        cli.require_auth()

    # We will exit early if the monitoring service is not running
    info = cli.service_info()        

    # If we allow failure, the response will be done
    if info:
        tty.debug("%s v.%s has status %s" %(info['id'],
            info['version'],
            info['status'])
        )
        return cli
        
    else:
        tty.debug("spack-monitor server not found, continuing as allow_fail is True.") 



class SpackMonitorClient:
    """The SpackMonitorClient is a handle to interact with a spack monitor
    server. We require the host url, along with the prefix to discover the
    service_info endpoint. If allow_fail is set to True, we will not exit
    on error with tty.fail given that a request is not successful.
    """
    def __init__(self, host=None, prefix="ms1", allow_fail=False):
        self.host = host or "http://127.0.0.1"
        self.baseurl = "%s/%s" % (self.host, prefix.strip("/"))
        self.token = os.environ.get("SPACKMON_TOKEN")
        self.username = os.environ.get("SPACKMON_USER")
        self.headers = {}

    def require_auth(self):
        """Require authentication, meaning that the token and username must
        not be unset
        """
        if not self.token or not self.username:
            tty.die("You are required to export SPACKMON_TOKEN and SPACKMON_USER")

    def set_header(self, name, value):
        self.headers.update({name: value})

    def set_basic_auth(self, username, password):
        """A wrapper to adding basic authentication to the Request"""
        auth_str = "%s:%s" % (username, password)
        auth_header = base64.b64encode(auth_str.encode("utf-8"))
        self.set_header("Authorization", "Basic %s" % auth_header.decode("utf-8"))

    def reset(self):
        """Reset and prepare for a new request.
        """
        if "Authorization" in self.headers:
            self.headers = {"Authorization": self.headers['Authorization']}
        else:
            self.headers = {}


    def prepare_request(self, endpoint, data, headers):
        """Given an endpoint url and data, prepare the request. If data
        is provided, urllib makes the request a POST
        """
        # Always reset headers for new request.
        self.reset()

        headers = headers or {}
        url = "%s/%s" % (self.baseurl, endpoint)

        # If we have data, the request will be POST
        if data:
            data = urllib.parse.urlencode(data)
            data = data.encode('ascii')

        return Request(url, data=data, headers=headers)

    def issue_request(self, request):
        """Given a prepared request, issue it. If we get an error, die. If
        there are times when we don't want to exit on error (but instead
        disable using the monitoring service) we could add that here.
        """
        try:
            response = urlopen(request)
        except URLError as e:
            msg = ""
            if hasattr(e, 'reason'):
                msg = e.reason 
            elif hasattr(e, 'code'):
                msg = e.code
            tty.die(msg)

        return response


    def do_request(self, endpoint, data=None, headers=None):
        """Do a request. If data is provided, it is POST, otherwise GET"""
        request = self.prepare_request(endpoint, data, headers)
        response = self.issue_request(request)
                        
        # A 401 response is a request for authentication
        if response.code != 401:
            return json.loads(response.read().decode('utf-8'))

        # Otherwise, authenticate the request and retry
        if self.authenticate_request(response):
            request = self.prepare_request(endpoint, data, self.headers)
            return self.issue_request(request)

        return response

    def authenticate_request(self, originalResponse):
        """Given a response, look for a Www-Authenticate header to parse. We
        return True/False to indicate if the request should be retried.
        """
        print(response)
        import IPython
        IPython.embed()
        sys.exit(0)

        authHeaderRaw = originalResponse.headers.get("Www-Authenticate")
        if not authHeaderRaw:

            return False

        # If we have a username and password, set basic auth automatically
        if self.token and self.username:
            self.set_basic_auth(self.username, self.token)

        headers = deepcopy(self.headers)
        if "Authorization" not in headers:
            logger.error(
                "This endpoint requires a token. Please set "
                "client.set_basic_auth(username, password) first "
                "or export them to the environment."
            )
            return False

        # Prepare request to retry
        h = parse_auth_header(authHeaderRaw)
        headers.update({"service": h.Service, "Accept": "application/json", "User-Agent": "spackmoncli"})

        # Currently we don't set a scope (it defaults to build)
        authResponse = self.session.request("GET", h.Realm, headers=headers)
        if authResponse.status_code != 200:
            return False
            
        # Request the token
        info = authResponse.json()
        token = info.get("token")
        if not token:
            token = info.get("access_token")

        # Set the token to the original request and retry
        self.headers.update({"Authorization": "Bearer %s" % token})
        return True


    # Functions correspond to endpoints
    def service_info(self):
        """get the service information endpoint"""
        # Base endpoint provides service info
        return self.do_request("")

    def upload_specfile(self, filename):
        """Given a spec file (must be json) upload to the UploadSpec endpoint"""
        # We load as json just to validate it
        spec = read_json(filename)
        return self.do_request("config/upload/", "POST", data=json.dumps(spec))

# Helper functions

def parse_auth_header(authHeaderRaw):
    """parse authentication header into pieces"""
    regex = re.compile('([a-zA-z]+)="(.+?)"')
    matches = regex.findall(authHeaderRaw)
    lookup = dict()
    for match in matches:
        lookup[match[0]] = match[1]
    return authHeader(lookup)


class authHeader:
    def __init__(self, lookup):
        """Given a dictionary of values, match them to class attributes"""
        for key in lookup:
            if key in ["realm", "service", "scope"]:
                setattr(self, key.capitalize(), lookup[key])

def read_file(filename):
    with open(filename, 'r') as fd:
        content = fd.read()
    return content
        
def read_json(filename):
    return json.loads(read_file(filename))
