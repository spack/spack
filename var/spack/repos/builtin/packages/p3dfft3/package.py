# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class P3dfft3(AutotoolsPackage):
    """P3DFFT++ (a.k.a. P3DFFT v. 3) is a new generation of P3DFFT library
    that aims to provide a comprehensive framework for simulating multiscale
    phenomena. It takes the essence of P3DFFT further by creating an
    extensible, modular structure uniquely adaptable to a greater range
    of use cases."""

    homepage = "https://www.p3dfft.net"
    url      = "https://github.com/sdsc/p3dfft.3/archive/master.tar.gz"
    git      = "https://github.com/sdsc/p3dfft.3"

    version('develop', branch='master')
    version('3.0.0', commit='b25205d5695abd0dd637fe607c36a8a5c99c7a08')

    variant('fftw', default=True,
            description='Builds with FFTW library')
    variant('essl', default=False,
            description='Builds with ESSL library')
    variant('mpi', default=True,
            description="Enable MPI support.")
    variant('openmp', default=False,
            description="Enable OpenMP support.")
    variant('measure', default=False,
            description="Define if you want to use"
                        "the measure fftw planner flag")
    variant('estimate', default=False,
            description="Define if you want to"
                        "use the estimate fftw planner flag")
    variant('patient', default=False,
            description="Define if you want to"
                        "use the patient fftw planner flag")

    depends_on('mpi', when='+mpi')
    depends_on('fftw', when='+fftw')
    depends_on('essl', when='+essl')
    depends_on('openmp', when='+openmp')

    def configure_args(self):
        args = []

        if '%gcc' in self.spec:
            args.append('--enable-gnu')

        if '%intel' in self.spec:
            args.append('--enable-intel')

        if '+mpi' in self.spec:
            args.append('CC=%s' % self.spec['mpi'].mpicc)
            args.append('CXX=%s' % self.spec['mpi'].mpicxx)
            args.append('FC=%s' % self.spec['mpi'].mpifc)
            args.append('CFLAGS=-L%s' % self.spec['mpi'].prefix.lib)
            args.append('CXXLAGS=-L%s' % self.spec['mpi'].prefix.lib)

        if '+openmpi' in self.spec:
            args.append('--enable-openmpi')

        if '+fftw' in self.spec:
            args.append('--enable-fftw')

            if '@:3.0.0' in self.spec:
                args.append('--with-fftw-lib=%s' %
                            self.spec['fftw'].prefix.lib)
                args.append('--with-fftw-inc=%s' %
                            self.spec['fftw'].prefix.include)
            else:
                args.append('--with-fftw=%s' % self.spec['fftw'].prefix)

            if 'fftw+measure' in self.spec:
                args.append('--enable-fftwmeasure')
            if 'fftw+estimate' in self.spec:
                args.append('--enable-fftwestimate')
            if 'fftw+patient' in self.spec:
                args.append('--enable-fftwpatient')

        if '+essl' in self.spec:
            args.append('--enable-essl')
            args.append('--with-essl-lib=%s' %
                        self.spec['essl'].prefix.lib)
            args.append('--with-essl-inc=%s' %
                        self.spec['essl'].prefix.include)

        if '+mkl' in self.spec:
            args.append('--enable-mkl')
            args.append('--with-mkl-lib=%s' % self.spec['mkl'].prefix.lib)
            args.append('--with-mkl-inc=%s' % self.spec['mkl'].prefix.include)

        return args
