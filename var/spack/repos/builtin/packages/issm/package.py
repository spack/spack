##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
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

# TODO:
# 1. I don't have MATLAB, so no way to test MATLAB version.


class Issm(Package):
    """Issm is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "https://issm.jpl.nasa.gov"
    url      = "https://github.com/issm/issm/tarball/v2.7.1"

    maintainers = ['citibeth']

    version('svn-head', svn='http://issm.ess.uci.edu/svn/issm/issm/trunk')

    variant('python', default=True, description='Build Python extension (requires Python, Numpy, etc)')
    variant('matlab', default=False, description='Build MATLAB extension')

    extends('python', when='+python')

    depends_on("autoconf")
    depends_on("mpi")
    depends_on("petsc")
    depends_on("scalapack")
    depends_on("mumps")
    depends_on("metis")

    # depends_on("m1qn3")
    # depends_on("triangle")

    depends_on("python@2:", when="+python")
    depends_on("py-nose", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-scipy", when="+python")
    # depends_on("py-netcdf", when="+python")

    depends_on("matlab", when="+matlab")

    def install(self, spec, prefix):
        mpi_dir = spec['mpi'].prefix
        os.environ['CC'] = os.path.join(mpi_dir, 'bin', 'mpicc')
        os.environ['CXX'] = os.path.join(mpi_dir, 'bin', 'mpicxx')
        os.environ['F77'] = os.path.join(mpi_dir, 'bin', 'mpif77')

        configure_args = [
            "--prefix=%s" % prefix,
            "--with-triangle-dir=%s" % spec['triangle'].prefix,
            "--with-petsc-dir=%s" % spec['petsc'].prefix,
            "--with-scalapack-dir=%s" % spec['scalapack'].prefix,
            "--with-mumps-dir=%s" % spec['mumps'].prefix,
            "--with-metis-dir=%s" % spec['metis'].prefix,
            "--with-m1qn3-dir=%s" % spec['m1qn3'].prefix]

        if '+python' in spec:
            config_args.append(
                "--with-python-dir=%s" % spec['python'].prefix)
            config_args.append(
                "--with-python-numpy-dir=%s" % spec['py-numpy'].prefix)

        if '+matlab' in spec:
            configure_args.append(
                "--with-matlab-dir=%s" % spec['matlab'].prefix)

        autoreconf('-iv')
        configure(*configure_args)
        make()
        make("install")
