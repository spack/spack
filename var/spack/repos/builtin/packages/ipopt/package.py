##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Ipopt(Package):
    """Ipopt (Interior Point OPTimizer, pronounced eye-pea-Opt) is a
       software package for large-scale nonlinear optimization."""
    homepage = "https://projects.coin-or.org/Ipopt"
    url      = "http://www.coin-or.org/download/source/Ipopt/Ipopt-3.12.4.tgz"

    version('3.12.4', '12a8ecaff8dd90025ddea6c65b49cb03')
    version('3.12.3', 'c560cbfa9cbf62acf8b485823c255a1b')
    version('3.12.2', 'ec1e855257d7de09e122c446506fb00d')
    version('3.12.1', 'ceaf895ce80c77778f2cab68ba9f17f3')
    version('3.12.0', 'f7dfc3aa106a6711a85214de7595e827')

    depends_on("blas")
    depends_on("lapack")
    depends_on("pkg-config", type='build')
    depends_on("mumps+double~mpi")

    def install(self, spec, prefix):
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

        configure_args = [
            "--prefix=%s" % prefix,
            "--with-mumps-incdir=%s" % mumps_dir.include,
            "--with-mumps-lib=%s" % mumps_libcmd,
            "--enable-shared",
            "--with-blas-incdir=%s" % blas_dir.include,
            "--with-blas-lib=%s" % blas_lib,
            "--with-lapack-incdir=%s" % lapack_dir.include,
            "--with-lapack-lib=%s" % lapack_lib
        ]

        configure(*configure_args)

        # IPOPT does not build correctly in parallel on OS X
        make(parallel=False)
        make("test", parallel=False)
        make("install", parallel=False)
