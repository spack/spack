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
import re
import yaml

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.cmd
import spack.config
from spack.dependency import default_deptype
from spack.error import SpackError
from spack.graph import graph_dot
from spack.paths import etc_path
from spack.spec import Spec
from spack.util.spec_set import CombinatorialSpecSet


description = "check if binaries need to be rebuilt"
section = "developer"
level = "long"


_pkg_match_regex = re.compile(r'packages[/\\]([^/\\]+)[/\\]package\.py')
_pkg_yaml_match_regex = re.compile(r'<a href=[^>]+\>\s*([^<]+)\s*\<')


def get_mirror_rebuilds(mirror_name, mirror_url, release_spec_set):
    tty.msg('Checking for built specs on %s' % mirror_name)

    # FIXME: Can uncomment once changes to buildcache are accepted...
    # build_cache_dir = bindist.build_cache_directory(mirror_url)
    build_cache_dir = os.path.join(mirror_url, 'build_cache')

    # First fetch the index.json
    index_path = os.path.join(build_cache_dir, 'index.json')
    index_contents = None

    try:
        url = urlopen(index_path)
    except URLError as urlErr:
        tty.error('Unable to open url %s' % index_path)
        tty.error(urlErr)
        return None
    except Exception as expn:
        tty.error('Error getting index from mirror')
        tty.error(expn)
        return None

    index_contents = url.read()

    if not index_contents:
        tty.error('Unable to read index from mirror')
        return None

    remote_pkg_index = json.loads(index_contents)

    rebuild_list = []

    for release_spec in release_spec_set:
        pkg_name = release_spec.name
        pkg_version = release_spec.version
        pkg_short_hash = release_spec.dag_hash()
        release_spec.concretize()
        pkg_full_hash = release_spec.full_hash()

        print('Checking %s-%s' % (pkg_name, pkg_version))

        if pkg_short_hash in remote_pkg_index:
            # At least remote binary mirror knows about it, so if the
            # full_hash doesn't match (or remote end doesn't know about
            # the full_hash), then we trigger a rebuild.
            remote_pkg_info = remote_pkg_index[pkg_short_hash]
            if not 'full_hash' in remote_pkg_info or \
                remote_pkg_info['full_hash'] != pkg_full_hash:
                    rebuild_list.append({
                        'short_spec': release_spec.short_spec,
                        'short_hash': pkg_short_hash
                    })
        else:
            # remote binary mirror doesn't know about this package, we
            # should probably just rebuild it
            rebuild_list.append({
                'short_spec': release_spec.short_spec,
                'short_hash': pkg_short_hash
            })

    return rebuild_list


def setup_parser(subparser):
    subparser.add_argument(
        '-m', '--mirror_url', default=None, help='Additional mirror url')

    subparser.add_argument(
        '-o', '--output_file', default='rebuilds.json',
        help='File where rebuild info should be written')

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.cmd.default_modify_scope(),
        help="configuration scope containing mirrors to check")


def checkbinaries(parser, args):
    release_specs_path = \
        os.path.join(etc_path, 'spack', 'defaults', 'release.yaml')

    release_spec_set = None

    with open(release_specs_path, 'r') as fin:
        release_specs_contents = fin.read()
        release_specs_yaml = yaml.load(release_specs_contents)

        # For now, turn off ignoring invalid specs, as it blocks iterating
        # the specs if the specified compilers can't be found.
        release_spec_set = CombinatorialSpecSet(release_specs_yaml,
                                                ignore_invalid=False)

    if not release_spec_set:
        tty.msg('No configured release specs, exiting.')
        return

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get('mirrors', scope=args.scope)

    if args.mirror_url:
        configured_mirrors['additionalMirrorUrl'] = args.mirror_url

    if not configured_mirrors:
        tty.msg('No configured mirrors, all done.')
        return

    # There are some binary mirrors, check each one against changed pkg list
    tty.msg('checking mirrors:')
    rebuilds = {}
    for mirror in configured_mirrors.keys():
        tty.msg('  %s -> %s' % (mirror, configured_mirrors[mirror]))
        mirror_url = configured_mirrors[mirror]
        mirror_rebuilds = get_mirror_rebuilds(mirror, mirror_url, release_spec_set)
        if len(mirror_rebuilds) > 0:
            rebuilds[mirror_url] = {
                'mirrorName': mirror,
                'mirrorUrl': mirror_url,
                'rebuildSpecs': mirror_rebuilds
            }

    with open(args.output_file, 'w') as outf:
        outf.write(json.dumps(rebuilds))


# from spack.dependency import default_deptype
# from spack.error import SpackError
# from spack.graph import graph_dot
# print('topologically sorted: ')
# graph_dot(rebuild['rebuildSpecs'], deptype=default_deptype, static=False)
