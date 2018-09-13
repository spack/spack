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

from llnl.util.tty.colify import colify
import llnl.util.tty as tty

import spack.repo

description = "list available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('package', metavar='PACKAGE',
                           help='package to list versions for')


def versions(parser, args):
    pkg = spack.repo.get(args.package)

    tty.msg('Safe versions (already checksummed):')

    safe_versions = pkg.versions

    if not safe_versions:
        print('  Found no versions for {0}'.format(pkg.name))
        tty.debug('Manually add versions to the package.')
    else:
        colify(sorted(safe_versions, reverse=True), indent=2)

    tty.msg('Remote versions (not yet checksummed):')

    fetched_versions = pkg.fetch_remote_versions()
    remote_versions = set(fetched_versions).difference(safe_versions)

    if not remote_versions:
        if not fetched_versions:
            print('  Found no versions for {0}'.format(pkg.name))
            tty.debug('Check the list_url and list_depth attributes of the '
                      'package to help Spack find versions.')
        else:
            print('  Found no unchecksummed versions for {0}'.format(pkg.name))
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)
