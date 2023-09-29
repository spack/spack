# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Exabayes(AutotoolsPackage):
    """ExaBayes is a software package for Bayesian tree inference. It is
       particularly suitable for large-scale analyses on computer clusters."""

    homepage = "https://cme.h-its.org/exelixis/web/software/exabayes/index.html"
    url      = "https://cme.h-its.org/exelixis/resource/download/software/exabayes-1.5.1.tar.gz"

    version('1.5.1', sha256='f75ce8d5cee4d241cadacd0f5f5612d783b9e9babff2a99c7e0c3819a94bbca9')

    variant('mpi', default=True, description='Enable MPI parallel support')

    depends_on('mpi', when='+mpi')

    # ExaBayes manual states the program succesfully compiles with GCC, version
    # 4.6 or greater, and Clang, version 3.2 or greater. The build fails when
    # GCC 7.1.0 is used.
    conflicts('%gcc@:4.5.4, 7.1.0:', when='@:1.5.0')
    conflicts('%clang@:3.1')

    # gcc 11.x has -std=gnu++17 by default, does not work to build exabayes, at least up to 1.5.1
    def flag_handler(self, name, flags):
        if self.spec.satisfies('%gcc@11:') and name == 'cxxflags':
            flags.append('-std=gnu++14')
        return (flags, None, None)

    # configure updated to better determine if MPI compiler available
    patch('configure_mpi.patch', level=0, when='@1.5.1: +mpi', )

    def configure_args(self):
        args = []
        if '+mpi' in self.spec:
            args.append('--enable-mpi')
        else:
            args.append('--disable-mpi')
        return args

    # don't do anything autoreconf as configure 
    # in exabayes is properly setup and
    # the autotools are not 
    def autoreconf(self, spec, prefix):
       return
