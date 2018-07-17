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
import os
import re
from datetime import datetime
from glob import glob

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

import spack.paths
from spack.util.executable import which

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='debug_command')
    sp.add_parser('create-db-tarball',
                  help="create a tarball of Spack's installation metadata")


def _debug_tarball_suffix():
    now = datetime.now()
    suffix = now.strftime('%Y-%m-%d-%H%M%S')

    git = which('git')
    if not git:
        return 'nobranch-nogit-%s' % suffix

    with working_dir(spack.paths.prefix):
        if not os.path.isdir('.git'):
            return 'nobranch.nogit.%s' % suffix

        # Get symbolic branch name and strip any special chars (mainly '/')
        symbolic = git(
            'rev-parse', '--abbrev-ref', '--short', 'HEAD', output=str).strip()
        symbolic = re.sub(r'[^\w.-]', '-', symbolic)

        # Get the commit hash too.
        commit = git(
            'rev-parse', '--short', 'HEAD', output=str).strip()

        if symbolic == commit:
            return "nobranch.%s.%s" % (commit, suffix)
        else:
            return "%s.%s.%s" % (symbolic, commit, suffix)


def create_db_tarball(args):
    tar = which('tar')
    tarball_name = "spack-db.%s.tar.gz" % _debug_tarball_suffix()
    tarball_path = os.path.abspath(tarball_name)

    base = os.path.basename(str(spack.store.root))
    transform_args = []
    if 'GNU' in tar('--version', output=str):
        transform_args = ['--transform', 's/^%s/%s/' % (base, tarball_name)]
    else:
        transform_args = ['-s', '/^%s/%s/' % (base, tarball_name)]

    wd = os.path.dirname(str(spack.store.root))
    with working_dir(wd):
        files = [spack.store.db._index_path]
        files += glob('%s/*/*/*/.spack/spec.yaml' % base)
        files = [os.path.relpath(f) for f in files]

        args = ['-czf', tarball_path]
        args += transform_args
        args += files
        tar(*args)

    tty.msg('Created %s' % tarball_name)


def debug(parser, args):
    action = {'create-db-tarball': create_db_tarball}
    action[args.debug_command](args)
