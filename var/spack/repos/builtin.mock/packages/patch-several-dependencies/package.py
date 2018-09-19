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


class PatchSeveralDependencies(Package):
    """Package that requries multiple patches on a dependency."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/patch-a-dependency-1.0.tar.gz"

    version('2.0', '0123456789abcdef0123456789abcdef')
    version('1.0', '0123456789abcdef0123456789abcdef')

    # demonstrate all the different ways to patch things

    # single patch file in repo
    depends_on('libelf', patches='foo.patch')

    # using a list of patches in one depends_on
    depends_on('libdwarf', patches=[
        patch('bar.patch'),                   # nested patch directive
        patch('baz.patch', when='@20111030')  # and with a conditional
    ], when='@1.0')  # with a depends_on conditional

    # URL patches
    depends_on('fake', patches=[
        # uncompressed URL patch
        patch('http://example.com/urlpatch.patch',
              sha256='abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234'),
        # compressed URL patch requires separate archive sha
        patch('http://example.com/urlpatch2.patch.gz',
              archive_sha256='abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd',
              sha256='1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd')
    ])

    def install(self, spec, prefix):
        pass
