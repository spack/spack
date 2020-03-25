# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMpiBenchmarks(MakefilePackage):
    """Intel(R) MPI Benchmarks provides a set of elementary benchmarks that conform to MPI-1, MPI-2, and MPI-3 standard. 
       You can run all of the supported benchmarks, or a subset specified in the command line using one executable file. 
       Use command-line parameters to specify various settings, such as time measurement, message lengths, and selection of communicators. """

    homepage = "https://software.intel.com/en-us/articles/intel-mpi-benchmarks"
    url      = "https://github.com/intel/mpi-benchmarks/archive/IMB-v2019.5.tar.gz"

    maintainers = ['carsonwoods']

    version('2019.5', sha256='61f8e872a3c3076af53007a68e4da3a8d66be2ba7a051dc21e626a4e2d26e651')
    version('2019.4', sha256='aeb336be10275c1a2f579b491b6631122876b461ac7148b1d0764f13b7552690')
    version('2019.3', sha256='4f256d11bfed9ca6166548486d61a062e67be61f13dd9f30690232720e185f31')
    version('2019.2', sha256='0bc2224a913073aaa5958f6ae08341e5fcd39cedc6722a09bfd4a3d7591a340b')

    depends_on('gmake', type='build')
    depends_on('mpi')

    def install(self, spec, prefix):
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifci

        install('all')


