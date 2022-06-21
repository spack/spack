# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Interact with a Spack Monitor Service. Derived from
https://github.com/spack/spack-monitor/blob/main/script/spackmoncli.py
"""

import base64
import hashlib
import os
import re
from datetime import datetime

try:
    from urllib.error import URLError
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import urlopen, Request, URLError  # type: ignore  # novm

from copy import deepcopy
from glob import glob

import llnl.util.tty as tty

import spack
import spack.config
import spack.hash_types as ht
import spack.main
import spack.paths
import spack.store
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml

# A global client to instantiate once
cli = None


def get_client(host, prefix="ms1", allow_fail=False, tags=None, save_local=False):
    """
    Get a monitor client for a particular host and prefix.

    If the client is not running, we exit early, unless allow_fail is set
    to true, indicating that we should continue the build even if the
    server is not present. Note that this client is defined globally as "cli"
    so we can istantiate it once (checking for credentials, etc.) and then
    always have access to it via spack.monitor.cli. Also note that
    typically, we call the monitor by way of hooks in spack.hooks.monitor.
    So if you want the monitor to have a new interaction with some part of
    the codebase, it's recommended to write a hook first, and then have
    the monitor use it.
    """
    global cli
    cli = SpackMonitorClient(host=host, prefix=prefix, allow_fail=allow_fail,
                             tags=tags, save_local=save_local)

    # Auth is always required unless we are saving locally
    if not save_local:
        cli.require_auth()

    # We will exit early if the monitoring service is not running, but
    # only if we aren't doing a local save
    if not save_local:
        info = cli.service_info()

        # If we allow failure, the response will be done
        if info:
            tty.debug("%s v.%s has status %s" % (
                info['id'],
                info['version'],
                info['status'])
            )
    return cli


def get_monitor_group(subparser):
    """
    Retrieve the monitor group for the argument parser.

    Since the monitor group is shared between commands, we provide a common
    function to generate the group for it. The user can pass the subparser, and
    the group is added, and returned.
    """
    # Monitoring via https://github.com/spack/spack-monitor
    monitor_group = subparser.add_argument_group()
    monitor_group.add_argument(
        '--monitor', action='store_true', dest='use_monitor', default=False,
        help="interact with a monitor server during builds.")
    monitor_group.add_argument(
        '--monitor-save-local', action='store_true', dest='monitor_save_local',
        default=False, help="save monitor results to .spack instead of server.")
    monitor_group.add_argument(
        '--monitor-tags', dest='monitor_tags', default=None,
        help="One or more (comma separated) tags for a build.")
    monitor_group.add_argument(
        '--monitor-keep-going', action='store_true', dest='monitor_keep_going',
        default=False, help="continue the build if a request to monitor fails.")
    monitor_group.add_argument(
        '--monitor-host', dest='monitor_host', default="http://127.0.0.1",
        help="If using a monitor, customize the host.")
    monitor_group.add_argument(
        '--monitor-prefix', dest='monitor_prefix', default="ms1",
        help="The API prefix for the monitor service.")
    return monitor_group


class SpackMonitorClient:
    """Client to interact with a spack monitor server.

    We require the host url, along with the prefix to discover the
    service_info endpoint. If allow_fail is set to True, we will not exit
    on error with tty.die given that a request is not successful. The spack
    version is one of the fields to uniquely identify a spec, so we add it
    to the client on init.
    """

    def __init__(self, host=None, prefix="ms1", allow_fail=False, tags=None,
                 save_local=False):
        # We can control setting an arbitrary version if needed
        sv = spack.main.get_version()
        self.spack_version = os.environ.get("SPACKMON_SPACK_VERSION") or sv

        self.host = host or "http://127.0.0.1"
        self.baseurl = "%s/%s" % (self.host, prefix.strip("/"))
        self.token = os.environ.get("SPACKMON_TOKEN")
        self.username = os.environ.get("SPACKMON_USER")
        self.headers = {}
        self.allow_fail = allow_fail
        self.capture_build_environment()
        self.tags = tags
        self.save_local = save_local

        # We key lookup of build_id by dag_hash
        self.build_ids = {}
        self.setup_save()

    def setup_save(self):
        """Given a local save "save_local" ensure the output directory exists.
        """
        if not self.save_local:
            return

        save_dir = spack.util.path.canonicalize_path(
            spack.config.get('config:monitor_dir', spack.paths.default_monitor_path)
        )

        # Name based on timestamp
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%s')
        self.save_dir = os.path.join(save_dir, now)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save(self, obj, filename):
        """
        Save a monitor json result to the save directory.
        """
        filename = os.path.join(self.save_dir, filename)
        write_json(obj, filename)
        return {"message": "Build saved locally to %s" % filename}

    def load_build_environment(self, spec):
        """
        Load a build environment from install_environment.json.

        If we are running an analyze command, we will need to load previously
        used build environment metadata from install_environment.json to capture
        what was done during the build.
        """
        if not hasattr(spec, "package") or not spec.package:
            tty.die("A spec must have a package to load the environment.")

        pkg_dir = os.path.dirname(spec.package.install_log_path)
        env_file = os.path.join(pkg_dir, "install_environment.json")
        build_environment = read_json(env_file)
        if not build_environment:
            tty.warn(
                "install_environment.json not found in package folder. "
                " This means that the current environment metadata will be used."
            )
        else:
            self.build_environment = build_environment

    def capture_build_environment(self):
        """
        Capture the environment for the build.

        This uses spack.util.environment.get_host_environment_metadata to do so.
        This is important because it's a unique identifier, along with the spec,
        for a Build. It should look something like this:

        {'host_os': 'ubuntu20.04',
         'platform': 'linux',
         'host_target': 'skylake',
         'hostname': 'vanessa-ThinkPad-T490s',
         'spack_version': '0.16.1-1455-52d5b55b65',
         'kernel_version': '#73-Ubuntu SMP Mon Jan 18 17:25:17 UTC 2021'}

        This is saved to a package install's metadata folder as
        install_environment.json, and can be loaded by the monitor for uploading
        data relevant to a later analysis.
        """
        from spack.util.environment import get_host_environment_metadata
        self.build_environment = get_host_environment_metadata()
        keys = list(self.build_environment.keys())

        # Allow to customize any of these values via the environment
        for key in keys:
            envar_name = "SPACKMON_%s" % key.upper()
            envar = os.environ.get(envar_name)
            if envar:
                self.build_environment[key] = envar

    def require_auth(self):
        """
        Require authentication.

        The token and username must not be unset
        """
        if not self.save_local and (not self.token or not self.username):
            tty.die("You are required to export SPACKMON_TOKEN and SPACKMON_USER")

    def set_header(self, name, value):
        self.headers.update({name: value})

    def set_basic_auth(self, username, password):
        """
        A wrapper to adding basic authentication to the Request
        """
        auth_str = "%s:%s" % (username, password)
        auth_header = base64.b64encode(auth_str.encode("utf-8"))
        self.set_header("Authorization", "Basic %s" % auth_header.decode("utf-8"))

    def reset(self):
        """
        Reset and prepare for a new request.
        """
        if "Authorization" in self.headers:
            self.headers = {"Authorization": self.headers['Authorization']}
        else:
            self.headers = {}

    def prepare_request(self, endpoint, data, headers):
        """
        Prepare a request given an endpoint, data, and headers.

        If data is provided, urllib makes the request a POST
        """
        # Always reset headers for new request.
        self.reset()

        # Preserve previously used auth token
        headers = headers or self.headers

        # The calling function can provide a full or partial url
        if not endpoint.startswith("http"):
            endpoint = "%s/%s" % (self.baseurl, endpoint)

        # If we have data, the request will be POST
        if data:
            if not isinstance(data, str):
                data = sjson.dump(data)
            data = data.encode('ascii')

        return Request(endpoint, data=data, headers=headers)

    def issue_request(self, request, retry=True):
        """
        Given a prepared request, issue it.

        If we get an error, die. If
        there are times when we don't want to exit on error (but instead
        disable using the monitoring service) we could add that here.
        """
        try:
            response = urlopen(request)
        except URLError as e:

            # If we have an authorization request, retry once with auth
            if hasattr(e, "code") and e.code == 401 and retry:
                if self.authenticate_request(e):
                    request = self.prepare_request(
                        e.url,
                        sjson.load(request.data.decode('utf-8')),
                        self.headers
                    )
                    return self.issue_request(request, False)

            # Handle permanent re-directs!
            elif hasattr(e, "code") and e.code == 308:
                location = e.headers.get('Location')

                request_data = None
                if request.data:
                    request_data = sjson.load(request.data.decode('utf-8'))[0]

                if location:
                    request = self.prepare_request(
                        location,
                        request_data,
                        self.headers
                    )
                    return self.issue_request(request, True)

            # Otherwise, relay the message and exit on error
            msg = ""
            if hasattr(e, 'reason'):
                msg = e.reason
            elif hasattr(e, 'code'):
                msg = e.code

            # If we can parse the message, try it
            try:
                msg += "\n%s" % e.read().decode("utf8", 'ignore')
            except Exception:
                pass

            if self.allow_fail:
                tty.warning("Request to %s was not successful, but continuing." % e.url)
                return

            tty.die(msg)

        return response

    def do_request(self, endpoint, data=None, headers=None, url=None):
        """
        Do the actual request.

        If data is provided, it is POST, otherwise GET.
        If an entire URL is provided, don't use the endpoint
        """
        request = self.prepare_request(endpoint, data, headers)

        # If we have an authorization error, we retry with
        response = self.issue_request(request)

        # A 200/201 response incidates success
        if response.code in [200, 201]:
            return sjson.load(response.read().decode('utf-8'))

        return response

    def authenticate_request(self, originalResponse):
        """
        Authenticate the request.

        Given a response (an HTTPError 401), look for a Www-Authenticate
        header to parse. We return True/False to indicate if the request
        should be retried.
        """
        authHeaderRaw = originalResponse.headers.get("Www-Authenticate")
        if not authHeaderRaw:
            return False

        # If we have a username and password, set basic auth automatically
        if self.token and self.username:
            self.set_basic_auth(self.username, self.token)

        headers = deepcopy(self.headers)
        if "Authorization" not in headers:
            tty.error(
                "This endpoint requires a token. Please set "
                "client.set_basic_auth(username, password) first "
                "or export them to the environment."
            )
            return False

        # Prepare request to retry
        h = parse_auth_header(authHeaderRaw)
        headers.update({
            "service": h.Service,
            "Accept": "application/json",
            "User-Agent": "spackmoncli"}
        )

        # Currently we don't set a scope (it defaults to build)
        authResponse = self.do_request(h.Realm, headers=headers)

        # Request the token
        token = authResponse.get("token")
        if not token:
            return False

        # Set the token to the original request and retry
        self.headers.update({"Authorization": "Bearer %s" % token})
        return True

    # Functions correspond to endpoints
    def service_info(self):
        """
        Get the service information endpoint
        """
        # Base endpoint provides service info
        return self.do_request("")

    def new_configuration(self, specs):
        """
        Given a list of specs, generate a new configuration for each.

        We return a lookup of specs with their package names. This assumes
        that we are only installing one version of each package. We aren't
        starting or creating any builds, so we don't need a build environment.
        """
        configs = {}

        # There should only be one spec generally (what cases would have >1?)
        for spec in specs:
            # Not sure if this is needed here, but I see it elsewhere
            if spec.name in spack.repo.path or spec.virtual:
                spec.concretize()

            # Remove extra level of nesting
            # This is the only place in Spack we still use full_hash, as `spack monitor`
            # requires specs with full_hash-keyed dependencies.
            as_dict = {"spec": spec.to_dict(hash=ht.full_hash)['spec'],
                       "spack_version": self.spack_version}

            if self.save_local:
                filename = "spec-%s-%s-config.json" % (spec.name, spec.version)
                self.save(as_dict, filename)
            else:
                response = self.do_request("specs/new/", data=sjson.dump(as_dict))
                configs[spec.package.name] = response.get('data', {})

        return configs

    def failed_concretization(self, specs):
        """
        Given a list of abstract specs, tell spack monitor concretization failed.
        """
        configs = {}

        # There should only be one spec generally (what cases would have >1?)
        for spec in specs:

            # update the spec to have build hash indicating that cannot be built
            meta = spec.to_dict()['spec']
            nodes = []
            for node in meta.get("nodes", []):
                node["full_hash"] = "FAILED_CONCRETIZATION"
                nodes.append(node)
            meta['nodes'] = nodes

            # We can't concretize / hash
            as_dict = {"spec": meta,
                       "spack_version": self.spack_version}

            if self.save_local:
                filename = "spec-%s-%s-config.json" % (spec.name, spec.version)
                self.save(as_dict, filename)
            else:
                response = self.do_request("specs/new/", data=sjson.dump(as_dict))
                configs[spec.package.name] = response.get('data', {})

        return configs

    def new_build(self, spec):
        """
        Create a new build.

        This means sending the hash of the spec to be built,
        along with the build environment. These two sets of data uniquely can
        identify the build, and we will add objects (the binaries produced) to
        it. We return the build id to the calling client.
        """
        return self.get_build_id(spec, return_response=True)

    def get_build_id(self, spec, return_response=False, spec_exists=True):
        """
        Retrieve a build id, either in the local cache, or query the server.
        """
        dag_hash = spec.dag_hash()
        if dag_hash in self.build_ids:
            return self.build_ids[dag_hash]

        # Prepare build environment data (including spack version)
        data = self.build_environment.copy()
        data['full_hash'] = dag_hash

        # If the build should be tagged, add it
        if self.tags:
            data['tags'] = self.tags

        # If we allow the spec to not exist (meaning we create it) we need to
        # include the full specfile here
        if not spec_exists:
            meta_dir = os.path.dirname(spec.package.install_log_path)
            spec_file = os.path.join(meta_dir, "spec.json")
            if os.path.exists(spec_file):
                data['spec'] = sjson.load(read_file(spec_file))
            else:
                spec_file = os.path.join(meta_dir, "spec.yaml")
                data['spec'] = syaml.load(read_file(spec_file))

        if self.save_local:
            return self.get_local_build_id(data, dag_hash, return_response)
        return self.get_server_build_id(data, dag_hash, return_response)

    def get_local_build_id(self, data, dag_hash, return_response):
        """
        Generate a local build id based on hashing the expected data
        """
        hasher = hashlib.md5()
        hasher.update(str(data).encode('utf-8'))
        bid = hasher.hexdigest()
        filename = "build-metadata-%s.json" % bid
        response = self.save(data, filename)
        if return_response:
            return response
        return bid

    def get_server_build_id(self, data, dag_hash, return_response=False):
        """
        Retrieve a build id from the spack monitor server
        """
        response = self.do_request("builds/new/", data=sjson.dump(data))

        # Add the build id to the lookup
        bid = self.build_ids[dag_hash] = response['data']['build']['build_id']
        self.build_ids[dag_hash] = bid

        # If the function is called directly, the user might want output
        if return_response:
            return response
        return bid

    def update_build(self, spec, status="SUCCESS"):
        """
        Update a build with a new status.

        This typically updates the relevant package to indicate a
        successful install. This endpoint can take a general status to update.
        """
        data = {"build_id": self.get_build_id(spec), "status": status}
        if self.save_local:
            filename = "build-%s-status.json" % data['build_id']
            return self.save(data, filename)

        return self.do_request("builds/update/", data=sjson.dump(data))

    def fail_task(self, spec):
        """Given a spec, mark it as failed. This means that Spack Monitor
        marks all dependencies as cancelled, unless they are already successful
        """
        return self.update_build(spec, status="FAILED")

    def cancel_task(self, spec):
        """Given a spec, mark it as cancelled.
        """
        return self.update_build(spec, status="CANCELLED")

    def send_analyze_metadata(self, pkg, metadata):
        """
        Send spack analyzer metadata to the spack monitor server.

        Given a dictionary of analyzers (with key as analyzer type, and
        value as the data) upload the analyzer output to Spack Monitor.
        Spack Monitor should either have a known understanding of the analyzer,
        or if not (the key is not recognized), it's assumed to be a dictionary
        of objects/files, each with attributes to be updated. E.g.,

        {"analyzer-name": {"object-file-path": {"feature1": "value1"}}}
        """
        # Prepare build environment data (including spack version)
        # Since the build might not have been generated, we include the spec
        data = {"build_id": self.get_build_id(pkg.spec, spec_exists=False),
                "metadata": metadata}
        return self.do_request("analyze/builds/", data=sjson.dump(data))

    def send_phase(self, pkg, phase_name, phase_output_file, status):
        """
        Send the result of a phase during install.

        Given a package, phase name, and status, update the monitor endpoint
        to alert of the status of the stage. This includes parsing the package
        metadata folder for phase output and error files
        """
        data = {"build_id": self.get_build_id(pkg.spec)}

        # Send output specific to the phase (does this include error?)
        data.update({"status": status,
                     "output": read_file(phase_output_file),
                     "phase_name": phase_name})

        if self.save_local:
            filename = "build-%s-phase-%s.json" % (data['build_id'], phase_name)
            return self.save(data, filename)

        return self.do_request("builds/phases/update/", data=sjson.dump(data))

    def upload_specfile(self, filename):
        """
        Upload a spec file to the spack monitor server.

        Given a spec file (must be json) upload to the UploadSpec endpoint.
        This function is not used in the spack to server workflow, but could
        be useful is Spack Monitor is intended to send an already generated
        file in some kind of separate analysis. For the environment file, we
        parse out SPACK_* variables to include.
        """
        # We load as json just to validate it
        spec = read_json(filename)
        data = {"spec": spec, "spack_verison": self.spack_version}

        if self.save_local:
            filename = "spec-%s-%s.json" % (spec.name, spec.version)
            return self.save(data, filename)

        return self.do_request("specs/new/", data=sjson.dump(data))

    def iter_read(self, pattern):
        """
        A helper to read json from a directory glob and return it loaded.
        """
        for filename in glob(pattern):
            basename = os.path.basename(filename)
            tty.info("Reading %s" % basename)
            yield read_json(filename)

    def upload_local_save(self, dirname):
        """
        Upload results from a locally saved directory to spack monitor.

        The general workflow will first include an install with save local:
        spack install --monitor --monitor-save-local
        And then a request to upload the root or specific directory.
        spack upload monitor ~/.spack/reports/monitor/<date>/
        """
        dirname = os.path.abspath(dirname)
        if not os.path.exists(dirname):
            tty.die("%s does not exist." % dirname)

        # We can't be sure the level of nesting the user has provided
        # So we walk recursively through and look for build metadata
        for subdir, dirs, files in os.walk(dirname):
            root = os.path.join(dirname, subdir)

            # A metadata file signals a monitor export
            metadata = glob("%s%sbuild-metadata*" % (root, os.sep))
            if not metadata or not files or not root or not subdir:
                continue
            self._upload_local_save(root)
        tty.info("Upload complete")

    def _upload_local_save(self, dirname):
        """
        Given a found metadata file, upload results to spack monitor.
        """
        # First find all the specs
        for spec in self.iter_read("%s%sspec*" % (dirname, os.sep)):
            self.do_request("specs/new/", data=sjson.dump(spec))

        # Load build metadata to generate an id
        metadata = glob("%s%sbuild-metadata*" % (dirname, os.sep))
        if not metadata:
            tty.die("Build metadata file(s) missing in %s" % dirname)

        # Create a build_id lookup based on hash
        hashes = {}
        for metafile in metadata:
            data = read_json(metafile)
            build = self.do_request("builds/new/", data=sjson.dump(data))
            localhash = os.path.basename(metafile).replace(".json", "")
            hashes[localhash.replace('build-metadata-', "")] = build

        # Next upload build phases
        for phase in self.iter_read("%s%sbuild*phase*" % (dirname, os.sep)):
            build_id = hashes[phase['build_id']]['data']['build']['build_id']
            phase['build_id'] = build_id
            self.do_request("builds/phases/update/", data=sjson.dump(phase))

        # Next find the status objects
        for status in self.iter_read("%s%sbuild*status*" % (dirname, os.sep)):
            build_id = hashes[status['build_id']]['data']['build']['build_id']
            status['build_id'] = build_id
            self.do_request("builds/update/", data=sjson.dump(status))


# Helper functions

def parse_auth_header(authHeaderRaw):
    """
    Parse an authentication header into relevant pieces
    """
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
    """
    Read a file, if it exists. Otherwise return None
    """
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as fd:
        content = fd.read()
    return content


def write_file(content, filename):
    """
    Write content to file
    """
    with open(filename, 'w') as fd:
        fd.writelines(content)
    return content


def write_json(obj, filename):
    """
    Write a json file, if the output directory exists.
    """
    if not os.path.exists(os.path.dirname(filename)):
        return
    return write_file(sjson.dump(obj), filename)


def read_json(filename):
    """
    Read a file and load into json, if it exists. Otherwise return None.
    """
    if not os.path.exists(filename):
        return
    return sjson.load(read_file(filename))
