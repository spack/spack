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


class Montage(MakefilePackage):
    """Montage is a toolkit for assembling Flexible Image Transport System
        (FITS) images into custom mosaics."""

    homepage = "http://montage.ipac.caltech.edu/"
    url      = "http://montage.ipac.caltech.edu/download/Montage_v5.0.tar.gz"

    version('5.0', sha256='72e034adb77c8a05ac40daf9d1923c66e94faa0b08d3d441256d9058fbc2aa34')

    variant('cfitsio',  default=False, description='use spack cfitsio library')
    variant('mpi',      default=False, description='Include MPI support') 
    variant('wcs',      default=False, description='use spack wcs library')

    depends_on('cfitsio', when='+mpi')
    depends_on('wcslib', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('freetype')

    def patch(self):
        filter_file(r"# MPICC  =", "MPICC  =", 'Montage/Makefile.LINUX',
                    when='+mpi')
        filter_file(r"# BINS =.*SBINS.*MBINS", "BINS = $(SBINS) $(MBINS)", 'Montage/Makefile.LINUX',
                    when='+mpi')
        filter_file('.*cfitsio.*', "", 'lib/src/Makefile')
        filter_file('.*freetype.*', "", 'lib/src/Makefile')
        #filter_file(r'.*cfitsio.*', '', 'lib/src/Makefile', when='+cfitsio')
        #filter_file(r'.*wcssubs3.9.0.montage.*', '', 'lib/src/Makefile',
       #             when='+wcslib')
        #filter_file(r'.wcs.h.', '<wcs.h>',
       #             'lib/src/two_plane_v1.1/two_plane.c', when='+wcslib')
        #filter_file(r'.fitsio.h.', '<fitsio.h>',
       #             'lib/src/two_plane_v1.1/two_plane.c', when='+wcslib')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('CPATH', self.prefix.include.wcslib)

    def install(self, spec, prefix):
        make("all")
        install_tree('bin', prefix.bin)
