# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Psm(MakefilePackage):
    """Intel Performance scaled messaging library"""

    homepage = "https://github.com/intel/psm"
    url      = "https://github.com/intel/psm/archive/v3.3.tar.gz"
    git      = "https://github.com/intel/psm.git"

    version('3.3', '031eb27688c932867d55054e76d00875', preferred=True)
    version('2017-04-28', commit='604758e')

    conflicts('%gcc@6:', when='@3.3')

    depends_on('libuuid')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('{DESTDIR}/usr/', '{LOCAL_PREFIX}/')

    def install(self, spec, prefix):
        make('LOCAL_PREFIX=%s' % prefix, 'install')
