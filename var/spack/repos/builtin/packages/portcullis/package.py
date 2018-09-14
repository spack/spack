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


class Portcullis(AutotoolsPackage):
    """PORTable CULLing of Invalid Splice junctions"""

    homepage = "https://github.com/maplesond/portcullis"
    url      = "https://github.com/maplesond/portcullis/archive/Release-1.1.2.tar.gz"

    version('1.1.2', '5c581a7f827ffeecfe68107b7fe27ed60108325fd2f86a79d93f61b328687749')

    depends_on('autoconf@2.53:', type='build')
    depends_on('automake@1.11:', type='build')
    depends_on('libtool@2.4.2:',  type='build')
    depends_on('m4', type='build')

    depends_on('zlib', type='build')
    depends_on('samtools', type='build')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))

    # later versions of py-sphinx don't get detected by the configure script
    depends_on('py-sphinx@1.3:1.4')

    def patch(self):
        # remove static linking to libstdc++
        filter_file(
            'AM_LDFLAGS="-static-libstdc++"',
            'AM_LDFLAGS=""',
            'configure.ac', string=True
        )

        # prevent install scripts from ruining our PYTHONPATH
        filter_file(
            'export PYTHONPATH=$(DESTDIR)$(pythondir)',
            'export PYTHONPATH="$(PYTHONPATH):$(DESTDIR)$(pythondir)"',
            'scripts/Makefile.am', string=True
        )

    def build(self, spec, prefix):
        # build manpages
        make('man')

        # run boost build script
        sh = which('sh')
        sh('build_boost.sh')
