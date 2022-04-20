# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Suntans(MakefilePackage):
    """The Stanford unstructured-grid, 
    nonhydrostatic, parallel coastal 
    ocean model. """

    homepage = "https://github.com/ofringer/suntans"
    url      = "https://github.com/ofringer/suntans/archive/master.zip"

    maintainers = ['ofringer', 'zyaj', 'mrayson', 'jadelson', 'lhxone']

    version('3.1', '971fbfee4a2a1e4b1f5722b5992debff69902f717dd0eb1e9162a92d4ac26dce')

    depends_on('libx11@1.6.3', type = ('build', 'run'))
    depends_on('mpi', type = ('build', 'run'))

    def edit(self, spec, prefix):
        env['MPIHOME'] = spec['openmpi'].prefix
        with working_dir('main'):
            makefile = FileFilter('Makefile')
            makefile.filter('XINC=.*', 'XINC= -I{0}'.format(spec['libx11'].prefix.include))
            makefile.filter('XLIBDIR = .*', 'XLIBDIR = {0}'.format(spec['libx11'].prefix.lib))
            makefile.filter('INCLUDES = .*', 'INCLUDES = $(PARMETISINCLUDE) $(TRIANGLEINCLUDE) $(NETCDFINCLUDE) $(XINC)')

    def build(self, spec, prefix):
        build_targets = ['CC = mpicc']
        with working_dir('main'):
            make('sunplot')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.include)
        with working_dir('main'):
            install('sunplot', prefix.bin)
            install('*.h', prefix.include)
