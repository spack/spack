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
