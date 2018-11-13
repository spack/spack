# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hpctoolkit(Package):
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"
    git      = "https://github.com/HPCToolkit/hpctoolkit.git"

    version('master')
    version('2017.06', tag='release-2017.06')

    variant('mpi', default=True, description='Enable MPI supoort')
    variant('papi', default=True, description='Enable PAPI counter support')

    depends_on('papi', when='+papi')
    depends_on('mpi', when='+mpi')
    depends_on('hpctoolkit-externals@2017.06', when='@2017.06')
    depends_on('hpctoolkit-externals@master', when='@master')

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   'CXX=%s' % self.compiler.cxx,
                   '--with-externals=%s' % spec['hpctoolkit-externals'].prefix]

        if '+mpi' in spec:
            options.extend(['MPICXX=%s' % spec['mpi'].mpicxx])

        if '+papi' in spec:
            options.extend(['--with-papi=%s' % spec['papi'].prefix])

        # TODO: BG-Q configure option
        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make('install')
