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


def get_remote_index(mirror_url):
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

    return json.loads(index_contents)


def get_mirror_rebuilds(mirror_name, mirror_url, release_spec_set):
    tty.msg('Checking for built specs on %s' % mirror_name)

    remote_pkg_index = get_remote_index(mirror_url)

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
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='check_command')

    # Create
    full_check = sp.add_parser('full', help=check_all.__doc__)
    full_check.add_argument(
        '-m', '--mirror_url', default=None, help='Additional mirror url')

    full_check.add_argument(
        '-o', '--output_file', default='rebuilds.json',
        help='File where rebuild info should be written')

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    full_check.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.cmd.default_modify_scope(),
        help="configuration scope containing mirrors to check")


    single_check = sp.add_parser('single', help=check_single.__doc__)
    single_check.add_argument(
        '-s', '--spec', default=None, help='spec to check')

    single_check.add_argument(
        '-m', '--mirror-url', default=None, help=' url of mirror to check')


def check_all(args):
    """Check full release spec-set against remote binaries mirrors
       and build a list of all specs that need to be rebuilt on each
       mirror."""
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


def check_single(args):
    """Check a single spec against a single remote binary mirror to see if
       it needs to be rebuilt."""
    spec_to_check = Spec(args.spec)

    if not spec_to_check:
        raise SpackError('Must provide spec to check against remote mirror')

    mirror_url = args.mirror_url

    if not mirror_url:
        raise SpackError('Must provide url of remote binary mirror')

    remote_pkg_index = get_remote_index(mirror_url)

    pkg_name = spec_to_check.name
    pkg_version = spec_to_check.version
    pkg_short_hash = spec_to_check.dag_hash()
    spec_to_check.concretize()
    pkg_full_hash = spec_to_check.full_hash()

    if pkg_short_hash in remote_pkg_index:
        remote_pkg_info = remote_pkg_index[pkg_short_hash]
        if 'full_hash' in remote_pkg_info:
            if remote_pkg_info['full_hash'] == pkg_full_hash:
                tty.msg('%s up to date' % spec_to_check)
            else:
                tty.msg('%s needs rebuild to full_hash mismatch')
        else:
            msg = '%s,%s full_hash not present' % (spec_to_check, mirror_url)
            tty.msg(msg)
    else:
        msg = '%s,%s package not present' % (spec_to_check, mirror_url)
        tty.msg(msg)


def check_binaries(parser, args):
    action = {
        'full': check_all,
        'single': check_single
    }

    action[args.check_command](args)
