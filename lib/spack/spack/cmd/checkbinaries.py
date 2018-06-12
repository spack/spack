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

import spack.cmd
import spack.config
from spack.error import SpackError
from spack.spec import Spec
from spack.util.executable import which


description = "check if binaries need to be rebuilt"
section = "developer"
level = "long"


_buildcache_path = os.path.join('build_cache')
_pkg_match_regex = re.compile(r'packages[/\\]([^/\\]+)[/\\]package\.py')
_pkg_yaml_match_regex = re.compile(r'<a href=[^>]+\>\s*([^<]+)\s*\<')


def changed_package_files(args):
    """Get list of changed package.py files in the Spack repository."""

    git = which('git', required=True)

    range = "{0}...".format(args.base)

    git_args = [
        # Add changed files committed since branching off of develop
        ['diff', '--name-only', '--diff-filter=ACMR', range],
        # Add changed files that have been staged but not yet committed
        ['diff', '--name-only', '--diff-filter=ACMR', '--cached'],
        # Add changed files that are unstaged
        ['diff', '--name-only', '--diff-filter=ACMR'],
    ]

    changed = set()

    for arg_list in git_args:
        files = git(*arg_list, output=str).split('\n')

        for f in files:
            # Look only for modified package.py files
            m = _pkg_match_regex.search(f)
            if m:
                changed.add(m.group(1))

    return sorted(changed)


def compute_local_hash(pkg_name, spec_yaml):
    local_spec = Spec.from_yaml(spec_yaml)
    tty.msg('local dag hash for %s: %s' % (pkg_name, local_spec.dag_hash()))
    local_spec.concretize()
    return local_spec.full_hash()


def compute_remote_hash(pkg_name, spec_yaml):
    parsed_yaml = yaml.load(spec_yaml)
    if 'full_hash' in parsed_yaml:
        return parsed_yaml['full_hash']

    msg = 'Binary mirror yaml file is missing full_hash attribute, aborting'
    raise SpackError(msg)


def check_needs_rebuild(pkg_name, spec_yaml):
    local_pkg_hash = compute_local_hash(pkg_name, spec_yaml)
    remote_pkg_hash = compute_remote_hash(pkg_name, spec_yaml)

    tty.msg('  %s' % pkg_name)
    tty.msg('    local hash: %s' % local_pkg_hash)
    tty.msg('    remote hash: %s' % remote_pkg_hash)

    if local_pkg_hash != remote_pkg_hash:
        return True

    return False


def parse_yaml_list(index_html_contents):
    result = []
    match_list = _pkg_yaml_match_regex.findall(index_html_contents)
    if match_list:
        result = match_list
    return result


def get_mirror_rebuilds(mirror_name, mirror_url, pkg_change_set):
    tty.msg('Checking for built specs on %s' % mirror_name)

    # First fetch the index.html
    index_path = os.path.join(mirror_url, _buildcache_path, 'index.html')
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
        tty.error('Unable to retrieve index from mirror')
        return None

    yaml_list = parse_yaml_list(index_contents)

    rebuild_list = []

    for pkg_name in pkg_change_set:
        tty.msg('yamls associated with %s' % pkg_name)

        for pkg_yaml in yaml_list:
            try:
                pkg_yaml.index('-%s-' % pkg_name)
                tty.msg('  %s' % pkg_yaml)
            except Exception as expn:
                continue

            yaml_path = os.path.join(mirror_url, _buildcache_path, pkg_yaml)
            yaml_contents = None

            try:
                yaml_url = urlopen(yaml_path)
            except URLError as urlErr:
                tty.error('Unable to open yaml url %s' % yaml_path)
                tty.error('Mirror (%s: %s)' % (mirror_name, mirror_url))
                tty.error(urlErr)
                return None
            except Exception as expn:
                tty.error('Error getting yaml file: %s' % yaml_path)
                tty.error('Mirror (%s: %s)' % (mirror_name, mirror_url))
                tty.error(expn)
                return None

            yaml_contents = yaml_url.read()

            if not yaml_contents:
                tty.error('Error getting yaml contents: %s' % yaml_path)
                tty.error('Mirror (%s: %s)' % (mirror_name, mirror_url))
                return None

            needs_rebuild = check_needs_rebuild(pkg_name, yaml_contents)

            if needs_rebuild:
                rebuild_list.append(pkg_yaml)

    return rebuild_list


def setup_parser(subparser):
    subparser.add_argument(
        '-b', '--base', action='store', default='develop',
        help="select base branch for collecting list of modified files")

    subparser.add_argument(
        '-m', '--mirror_url', default=None, help='Additional mirror url')

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    subparser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.cmd.default_modify_scope(),
        help="configuration scope containing mirrors to check")


def checkbinaries(parser, args):
    # First step is to find package.py files which have changed
    change_set = changed_package_files(args)
    if not change_set:
        tty.msg('No changed package files, all done.')
        return

    tty.msg('\nchanged packages:')
    for f in change_set:
        tty.msg('  %s' % f)
    tty.msg('\n')

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get('mirrors', scope=args.scope)

    if args.mirror_url:
        configured_mirrors['additionalMirrorUrl'] = args.mirror_url

    if not configured_mirrors:
        tty.msg('No configured mirrors, all done.')
        return

    # There are some binary mirrors, check each one against changed pkg list
    tty.msg('checking mirrors:')
    rebuilds = []
    for mirror in configured_mirrors.keys():
        tty.msg('  %s -> %s' % (mirror, configured_mirrors[mirror]))
        mirror_url = configured_mirrors[mirror]
        mirror_rebuilds = get_mirror_rebuilds(mirror, mirror_url, change_set)
        if len(mirror_rebuilds) > 0:
            rebuilds.append({
                'mirrorName': mirror,
                'mirrorUrl': configured_mirrors[mirror],
                'rebuildSpecs': mirror_rebuilds
            })

    tty.msg('')
    tty.msg(json.dumps(rebuilds))
    tty.msg('')
