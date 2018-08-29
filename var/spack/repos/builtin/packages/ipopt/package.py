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


class Ipopt(AutotoolsPackage):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://projects.coin-or.org/Ipopt"
    url      = "http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.4.tgz"

    version('3.12.10', 'e1a3ad09e41edbfe41948555ece0bdc78757a5ca764b6be5a9a127af2e202d2e')
    version('3.12.9', '8ff3fe1a8560896fc5559839a87c2530cac4ed231b0806e487bfd3cf2d294ab8')
    version('3.12.8', '62c6de314220851b8f4d6898b9ae8cf0a8f1e96b68429be1161f8550bb7ddb03')
    version('3.12.7', '2a36e4a04717a8ed7012ac7d1253ae4ffbc1a8fd')
    version('3.12.6', 'ed4072427fab786fcf6082fe7e6f6c2ed9b5e6f8')
    version('3.12.5', '3f63ddfff517235ead17af6cceb426ca858dda37')
    version('3.12.4', '12a8ecaff8dd90025ddea6c65b49cb03')
    version('3.12.3', 'c560cbfa9cbf62acf8b485823c255a1b')
    version('3.12.2', 'ec1e855257d7de09e122c446506fb00d')
    version('3.12.1', 'ceaf895ce80c77778f2cab68ba9f17f3')
    version('3.12.0', 'f7dfc3aa106a6711a85214de7595e827')

    variant('coinhsl', default=False,
            description="Build with Coin Harwell Subroutine Libraries")
    variant('metis', default=False,
            description="Build with METIS partitioning support")

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkgconfig", type='build')
    depends_on("mumps+double~mpi")
    depends_on('coinhsl', when='+coinhsl')
    depends_on('metis@4.0:', when='+metis')

    patch('ipopt_ppc_build.patch', when='arch=ppc64le')

    flag_handler = AutotoolsPackage.build_system_flags
    build_directory = 'spack-build'

    # IPOPT does not build correctly in parallel on OS X
    parallel = False

    def configure_args(self):
        spec = self.spec
        # Dependency directories
        blas_dir = spec['blas'].prefix
        lapack_dir = spec['lapack'].prefix
        mumps_dir = spec['mumps'].prefix

        # Add directory with fake MPI headers in sequential MUMPS
        # install to header search path
        mumps_flags = "-ldmumps -lmumps_common -lpord -lmpiseq"
        mumps_libcmd = "-L%s " % mumps_dir.lib + mumps_flags

        blas_lib = spec['blas'].libs.ld_flags
        lapack_lib = spec['lapack'].libs.ld_flags

        args = [
            "--prefix=%s" % self.prefix,
            "--with-mumps-incdir=%s" % mumps_dir.include,
            "--with-mumps-lib=%s" % mumps_libcmd,
            "--enable-shared",
            "coin_skip_warn_cxxflags=yes",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
        ]

        if 'coinhsl' in spec:
            args.extend([
                '--with-hsl-lib=%s' % spec['coinhsl'].libs.ld_flags,
                '--with-hsl-incdir=%s' % spec['coinhsl'].prefix.include])

        if 'metis' in spec:
            args.extend([
                '--with-metis-lib=%s' % spec['metis'].libs.ld_flags,
                '--with-metis-incdir=%s' % spec['metis'].prefix.include])

        return args
