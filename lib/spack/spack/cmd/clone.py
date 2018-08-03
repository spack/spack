##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, working_dir

import spack.paths
from spack.util.executable import ProcessError, which

_SPACK_UPSTREAM = 'https://github.com/spack/spack'

description = "create a new installation of spack in another prefix"
section = "admin"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-r', '--remote', action='store', dest='remote',
        help="name of the remote to clone from", default='origin')
    subparser.add_argument(
        'prefix',
        help="name of prefix where we should install spack")


def get_origin_info(remote):
    git_dir = os.path.join(spack.paths.prefix, '.git')
    git = which('git', required=True)
    try:
        branch = git('symbolic-ref', '--short', 'HEAD', output=str)
    except ProcessError:
        branch = 'develop'
        tty.warn('No branch found; using default branch: %s' % branch)
    if remote == 'origin' and \
       branch not in ('master', 'develop'):
        branch = 'develop'
        tty.warn('Unknown branch found; using default branch: %s' % branch)
    try:
        origin_url = git(
            '--git-dir=%s' % git_dir,
            'config', '--get', 'remote.%s.url' % remote,
            output=str)
    except ProcessError:
        origin_url = _SPACK_UPSTREAM
        tty.warn('No git repository found; '
                 'using default upstream URL: %s' % origin_url)
    return (origin_url.strip(), branch.strip())


def clone(parser, args):
    origin_url, branch = get_origin_info(args.remote)
    prefix = args.prefix

    tty.msg("Fetching spack from '%s': %s" % (args.remote, origin_url))

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    mkdirp(prefix)

    if os.path.exists(os.path.join(prefix, '.git')):
        tty.die("There already seems to be a git repository in %s" % prefix)

    files_in_the_way = os.listdir(prefix)
    if files_in_the_way:
        tty.die("There are already files there! "
                "Delete these files before boostrapping spack.",
                *files_in_the_way)

    tty.msg("Installing:",
            "%s/bin/spack" % prefix,
            "%s/lib/spack/..." % prefix)

    with working_dir(prefix):
        git = which('git', required=True)
        git('init', '--shared', '-q')
        git('remote', 'add', 'origin', origin_url)
        git('fetch', 'origin', '%s:refs/remotes/origin/%s' % (branch, branch),
            '-n', '-q')
        git('reset', '--hard', 'origin/%s' % branch, '-q')
        git('checkout', '-B', branch, 'origin/%s' % branch, '-q')

        tty.msg("Successfully created a new spack in %s" % prefix,
                "Run %s/bin/spack to use this installation." % prefix)
