##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class PyGpaw(PythonPackage):
    """GPAW is a density-functional theory (DFT) Python code based on the projector-augmented wave (PAW) method and the atomic simulation environment (ASE)."""

    homepage = "https://wiki.fysik.dtu.dk/gpaw/index.html"
    url      = "https://pypi.io/packages/source/g/gpaw/gpaw-1.3.0.tar.gz"

    version('1.3.0', '82e8c80e637696248db00b5713cdffd1')

    variant('mpi', default=True, description='Build with MPI support')
    variant('scalapack', default=False, description='Build with ScaLAPACK support')
    variant('fftw', default=True, description='Build with FFTW support')

    depends_on('mpi',when='+mpi',type=('build','link','run'))
    depends_on('python@2.6:')
    depends_on('py-ase',        type=('build', 'run'))
    depends_on('py-numpy +blas +lapack', type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('libxc',type=('build','link','run'))
    depends_on('blas',type=('build','link','run'))
    depends_on('lapack',type=('build','link','run'))
    depends_on('fftw+mpi',when='+fftw +mpi')
    depends_on('fftw~mpi',when='+fftw ~mpi')
    depends_on('scalapack',when='+scalapack')

    def patch(self):
        spec = self.spec
        compiler = self.compiler
        # For build notes see https://wiki.fysik.dtu.dk/gpaw/install.html

        libxc = spec['libxc']
        blas = spec['blas']
        lapack = spec['lapack']

        libs = blas.libs + lapack.libs + libxc.libs
        include_dirs = [blas.prefix.include,lapack.prefix.include,libxc.prefix.include]
        lib_dirs = [blas.prefix.lib,lapack.prefix.lib,libxc.prefix.lib]
        if '+mpi' in spec:
            libs += spec['mpi'].libs
            include_dirs.append(spec['mpi'].prefix.include)
            lib_dirs.append(spec['mpi'].prefix.lib)
        if '+scalapack' in spec:
            libs += spec['scalapack'].libs
            include_dirs.append(spec['scalapack'].prefix.include)
            lib_dirs.append(spec['scalapack'].prefix.lib)
        if '+fftw' in spec:
            libs += spec['fftw'].libs
            include_dirs.append(spec['fftw'].prefix.include)
            lib_dirs.append(spec['fftw'].prefix.lib)
        libs = list(libs.names)

        with open('customize.py', 'w') as f:
            f.write("libraries = {0}\n".format(repr(libs)))
            f.write("include_dirs = {0}\n".format(repr(include_dirs)))
            f.write("library_dirs = {0}\n".format(repr(lib_dirs)))
            f.write("extra_link_args += ['-Wl,-rpath={0}']\n".format(':'.join(self.rpath)))
            if '+mpi' in spec:
                f.write("define_macros += [('PARALLEL', '1')]\n")
                f.write("compiler='{0}'\n".format(spec['mpi'].mpicc))
                f.write("mpicompiler = '{0}'\n".format(spec['mpi'].mpicc))
                f.write("mpi_include_dirs = {0}\n".format(repr([spec['mpi'].prefix.include])))
                f.write("mpi_library_dirs = {0}\n".format(repr([spec['mpi'].prefix.lib])))
            else:
                f.write("compiler='{0}'\n".format(self.compiler.cc))
                f.write("mpicompiler = None\n")
            if '+scalapack' in spec:
              f.write("scalapack = True\n")
              f.write("define_macros += [('GPAW_NO_UNDERSCORE_CBLACS', '1')]\n")
              f.write("define_macros += [('GPAW_NO_UNDERSCORE_CSCALAPACK', '1')]\n")
