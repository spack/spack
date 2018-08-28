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
from spack import *


class GitUrlTopLevel(Package):
    """Mock package that top-level git and url attributes.

    This demonstrates how Spack infers fetch mechanisms from parameters
    to the ``version`` directive.

    """
    homepage = "http://www.git-fetch-example.com"

    git = 'https://example.com/some/git/repo'
    url = 'https://example.com/some/tarball-1.0.tar.gz'

    # These resolve to git fetchers
    version('develop', branch='develop')
    version('submodules', submodules=True)
    version('3.4', commit='abc34')
    version('3.3', branch='releases/v3.3', commit='abc33')
    version('3.2', branch='releases/v3.2')
    version('3.1', tag='v3.1', commit='abc31')
    version('3.0', tag='v3.0')

    # These resolve to URL fetchers
    version('2.3', 'abc23', url='https://www.example.com/foo2.3.tar.gz')
    version('2.2', sha256='abc22', url='https://www.example.com/foo2.2.tar.gz')
    version('2.1', sha256='abc21')
    version('2.0', 'abc20')

    # These result in a FetcherConflict b/c we can't tell what to use
    version('1.3', sha256='abc13', commit='abc13')
    version('1.2', sha512='abc12', branch='releases/v1.2')
    version('1.1', md5='abc11', tag='v1.1')
    version('1.0', 'abc11', tag='abc123')

    def install(self, spec, prefix):
        pass
