##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from __future__ import print_function

from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError

import json
import os
import sys

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.cmd
import spack.config
from spack.error import SpackError
from spack.paths import etc_path
from spack.spec import Spec
from spack.util.spec_set import CombinatorialSpecSet
import spack.util.spack_yaml as syaml


description = "check if binaries need to be rebuilt"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-m', '--mirror-url', default=None,
        help='Override any configured mirrors with this mirror url')

    subparser.add_argument(
        '-o', '--output-file', default=None,
        help='File where rebuild info should be written')

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.cmd.default_modify_scope(),
        help="configuration scope containing mirrors to check")

    subparser.add_argument(
        '-s', '--spec', default=None,
        help='Check single spec instead of building from release specs file')

    subparser.add_argument(
        '-n', '--no-index', action='store_true', default=False,
        help='Do not use buildcache index, instead retrieve .spec.yaml files')


def read_from_url(file_uri):
    file_contents = None

    try:
        url = urlopen(file_uri)
    except URLError as url_err:
        msg = 'Unable to open url {0} due to {1}'.format(
            file_uri, url_err.message)
        raise SpackError(msg)
    except Exception as expn:
        msg = 'Error getting file contents at {0} due to {1}'.format(
            file_uri, expn.message)
        raise SpackError(msg)

    file_contents = url.read()

    if not file_contents:
        msg = 'Unable to read file contents at {0}'.format(file_uri)
        raise SpackError(msg)

    return file_contents


def needs_rebuild(spec, mirror_url, buildcache_index):
    pkg_name = spec.name
    pkg_version = spec.version

    tty.msg('Checking {0}-{1}'.format(pkg_name, pkg_version))

    spec.concretize()
    pkg_hash = spec.dag_hash()
    pkg_full_hash = spec.full_hash()

    rebuild_spec = {
        'short_spec': spec.short_spec,
        'hash': pkg_hash
    }

    if buildcache_index:
        # just look in the index we already fetched
        if pkg_hash in buildcache_index:
            # At least remote binary mirror knows about it, so if the
            # full_hash doesn't match (or remote end doesn't know about
            # the full_hash), then we trigger a rebuild.
            remote_pkg_info = buildcache_index[pkg_hash]
            if ('full_hash' not in remote_pkg_info or
                remote_pkg_info['full_hash'] != pkg_full_hash):
                    return rebuild_spec
        else:
            # remote binary mirror doesn't know about this package, we
            # should probably just rebuild it
            return rebuild_spec
    else:
        # retrieve the .spec.yaml and look there instead
        build_cache_dir = bindist.build_cache_directory(mirror_url)
        spec_yaml_file_name = bindist.tarball_name(spec, '.spec.yaml')
        file_path = os.path.join(build_cache_dir, spec_yaml_file_name)
        try:
            yaml_contents = read_from_url(file_path)
        except SpackError:
            # let any kind of failure reading the .spec.yaml indicate rebuild
            return rebuild_spec
        spec_yaml = syaml.load(yaml_contents)

        if ('full_hash' not in spec_yaml or
            spec_yaml['full_hash'] != pkg_full_hash):
                return rebuild_spec

    return None


def get_remote_index(mirror_url):
    build_cache_dir = bindist.build_cache_directory(mirror_url)

    # First fetch the index.json
    index_path = os.path.join(build_cache_dir, 'index.json')
    index_contents = read_from_url(index_path)

    return json.loads(index_contents)


def check(mirrors, specs, no_index=False, output_file=None):
    rebuilds = {}
    for mirror in mirrors.keys():
        mirror_url = mirrors[mirror]
        tty.msg('Checking for built specs at %s' % mirror_url)

        rebuild_list = []
        remote_pkg_index = None
        if not no_index:
            remote_pkg_index = get_remote_index(mirror_url)

        for spec in specs:
            rebuild_spec = needs_rebuild(spec, mirror_url, remote_pkg_index)
            if rebuild_spec:
                rebuild_list.append(rebuild_spec)

        if rebuild_list:
            rebuilds[mirror_url] = {
                'mirrorName': mirror,
                'mirrorUrl': mirror_url,
                'rebuildSpecs': rebuild_list
            }

    if output_file:
        with open(output_file, 'w') as outf:
            outf.write(json.dumps(rebuilds))

    return 1 if rebuilds else 0


def check_binaries(parser, args):
    """
    Check specs (either a single spec from --spec, or else the full set of
    release specs) against remote binary mirror(s) to see if any need to be
    rebuilt.
    """
    if args.spec:
        specs = [Spec(args.spec)]
    else:
        release_specs_path = \
            os.path.join(etc_path, 'spack', 'defaults', 'release.yaml')
        specs = CombinatorialSpecSet.from_file(release_specs_path)

    if not specs:
        tty.msg('No specs provided, exiting.')
        sys.exit(0)

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get('mirrors', scope=args.scope)

    if args.mirror_url:
        configured_mirrors = {'additionalMirrorUrl': args.mirror_url}

    if not configured_mirrors:
        tty.msg('No mirrors provided, exiting.')
        sys.exit(0)

    no_index = args.no_index
    output_file = args.output_file

    sys.exit(check(configured_mirrors, specs, no_index, output_file))
