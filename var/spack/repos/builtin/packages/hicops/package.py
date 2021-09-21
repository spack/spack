# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hicops(Package):
    """HiCOPS is a software framework for accelerating database peptide search workflows on supercomputers.
    HiCOPS provided algorithm-independent parallelizations and optimizations can be extended into new HPC
    database search algorithms or scalably accelerate the existing ones.
    """

    homepage = "https://hicops.github.io/index"
    git = "https://github.com/hicops/hicops.git"
    maintainers = ['pcdslab', 'mhaseeb123', 'nessiecancode']

    version('release', branch='release')
    version('develop', branch='develop')

    # Build Options
    variant('USE_MPI', default='ON',
            description='CMake Option: Enable MPI support.',
            values=('ON', 'OFF'))
    variant('USE_TIMEMORY', default='OFF',
            description='CMake Option: Enable timemory interface. Requires timemory installation.',
            values=('ON', 'OFF'))
    variant('USE_MPIP_LIBRARY', default='OFF',
            description='CMake Option: Enables the MPIP data_tracker via Timemory. Requires timemory installation.',
            values=('ON', 'OFF'))
    variant('TAILFIT', default='ON',
            description='CMake Option: Use the tailfit method instead of Gumbelfit for e-value computation.',
            values=('ON', 'OFF'))
    variant('PROGRESS', default='ON',
            description='CMake Option: Display HiCOPS progress marks.',
            values=('ON', 'OFF'))
    variant('MAX_SEQ_LEN', default='60',
            description='CMake Option: Allowed maximum peptide sequence length.')
    variant('QALEN', default='100',
            description='CMake Option: Maximum number of top K peaks to keep when spectrum preprocess.')
    variant('QCHUNK', default='10000',
            description='CMake Option: Max size of each batch extracted from the dataset.')
    variant('MAX_HYPERSCORE', default='100',
            description='CMake Option: Maximum allowed hyperscore computed.')

    # Build Controls
    variant('CMAKE_BUILD_TYPE', default='RelWithDebInfo',
            description='CMake Build Control: Build type.',
            values=('Release', 'Debug', 'MinSizeRel', 'RelWithDebInfo'))
    variant('CMAKE_CXX_STANDARD', default='14',
            description='CMake Build Control: C++ standard.')

    depends_on('git', type='build', when='@release')
    depends_on('git', type='build', when='@develop')
    depends_on('boost')
    depends_on('py-numpy')
    depends_on('py-python-dateutil')
    depends_on('py-setuptools')
    depends_on('py-bottleneck')
    depends_on('py-pyparsing')
    depends_on('py-subprocess32')
    depends_on('py-six')
    depends_on('cmake@3.11:3.21.2')
    depends_on('py-setuptools-scm')
    depends_on('pkgconf')
    depends_on('py-et-xmlfile')
    depends_on('py-argparse')
    depends_on('py-cython')
    depends_on('py-cycler')
    depends_on('mpich')
    depends_on('py-pytz')
    depends_on('py-kiwisolver')
    depends_on('py-numexpr')
    depends_on('py-matplotlib')
    depends_on('py-jdcal')
    depends_on('py-pandas')
    depends_on('py-openpyxl')
    depends_on('python@3.7:3.9')

    conflicts('%gcc@:7.2')


    def setup_run_environment(self, env):
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        env.prepend_path('PATH', self.prefix.bin)
        env.prepend_path('PATH', self.prefix.tools)
        env.prepend_path('PATH', self.prefix.bin.tools)
        env.set('HICOPS_INSTALL', self.prefix)
        env.prepend_path("INCLUDE", self.prefix.include)



    def install(self, spec, prefix):
        spec = self.spec
        options = []

        options.extend([
            '-DUSE_MPI=ON',  # known issue: forced variant
            '-DUSE_TIMEMORY=%s' % str(spec.variants['USE_TIMEMORY'].value),
            '-DUSE_MPIP_LIBRARY=%s' % str(spec.variants['USE_MPIP_LIBRARY'].value),
            '-DTAILFIT=%s' % str(spec.variants['TAILFIT'].value),
            '-DPROGRESS=%s' % str(spec.variants['PROGRESS'].value),
            '-DMAX_SEQ_LEN=%i' % int(spec.variants['MAX_SEQ_LEN'].value),
            '-DQALEN=%i' % int(spec.variants['QALEN'].value),
            '-DQCHUNK=%i' % int(spec.variants['QCHUNK'].value),
            '-DMAX_HYPERSCORE=%i' % int(spec.variants['MAX_HYPERSCORE'].value),
            '-DCMAKE_BUILD_TYPE=%s' % str(spec.variants['CMAKE_BUILD_TYPE'].value),
            '-DCMAKE_CXX_STANDARD=%i' % int(spec.variants['CMAKE_CXX_STANDARD'].value),
            '-DCMAKE_INSTALL_PREFIX=%s' % str(self.prefix)
        ])
        cmake(*options)
        make()
        make('install')
