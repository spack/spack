# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unblur(AutotoolsPackage):
    """Unblur is used to align the frames of movies recorded on an electron
    microscope to reduce image blurring due to beam-induced motion."""

    homepage = "http://grigoriefflab.janelia.org/unblur"
    url      = "http://grigoriefflab.janelia.org/sites/default/files/unblur_1.0.2.tar.gz"

    version('1.0.2', 'b6e367061cd0cef1b62a391a6289f681')

    variant('openmp', default=True, description='Enable OpenMP support')
    variant('shared', default=True, description='Dynamic linking')

    depends_on('zlib')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('gsl')
    depends_on('jbigkit')
    depends_on('fftw@3:')
    # Requires Intel Fortran compiler
    conflicts('%gcc')
    conflicts('%pgi')
    conflicts('%clang')
    conflicts('%cce')
    conflicts('%xl')
    conflicts('%xl_r')
    conflicts('%nag')

    configure_directory = 'src'

    def patch(self):
        filter_file(r'<<<<<<<.*', '', 'src/missing')

    def configure_args(self):
        spec = self.spec
        return ['FC=ifort',
                'F77=ifort',
                '--enable-static={0}'
                .format('yes' if '~shared' in spec else 'no'),
                '--enable-openmp={0}'
                .format('yes' if '+openmp' in spec else 'no'),
                '--enable-optimisations=yes']

    def build(self, spec, prefix):
        with working_dir('src'):
            make(parallel=False)
