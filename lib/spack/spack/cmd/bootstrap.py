##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
from subprocess import check_call

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack
from spack.util.executable import which

description = "Create a new installation of spack in another prefix"

def setup_parser(subparser):
    subparser.add_argument('prefix', help="names of prefix where we should install spack")


def get_origin_url():
    git_dir = join_path(spack.prefix, '.git')
    git = which('git', required=True)
    origin_url = git(
        '--git-dir=%s' % git_dir, 'config', '--get', 'remote.origin.url',
        return_output=True)
    return origin_url.strip()


def bootstrap(parser, args):
    origin_url = get_origin_url()
    prefix = args.prefix

    tty.msg("Fetching spack from origin: %s" % origin_url)

    if os.path.isfile(prefix):
        tty.die("There is already a file at %s" % prefix)

    mkdirp(prefix)

    if os.path.exists(join_path(prefix, '.git')):
        tty.die("There already seems to be a git repository in %s" % prefix)

    files_in_the_way = os.listdir(prefix)
    if files_in_the_way:
        tty.die("There are already files there!  Delete these files before boostrapping spack.",
                *files_in_the_way)

    tty.msg("Installing:",
            "%s/bin/spack" % prefix,
            "%s/lib/spack/..." % prefix)

    os.chdir(prefix)
    git = which('git', required=True)
    git('init', '--shared', '-q')
    git('remote', 'add', 'origin', origin_url)
    git('fetch', 'origin', 'master:refs/remotes/origin/master', '-n', '-q')
    git('reset', '--hard', 'origin/master', '-q')

    tty.msg("Successfully created a new spack in %s" % prefix,
            "Run %s/bin/spack to use this installation." % prefix)
