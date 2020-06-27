# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import platform


class Lcals(MakefilePackage):
    """LCALS ("Livermore Compiler Analysis Loop Suite") is a collection of loop
       kernels based, in part, on historical "Livermore Loops" benchmarks
       (See the 1986 technical report: "The Livermore Fortran Kernels:
        A Computer Test of the Numerical Performance Range",
        by Frank H. McMahon, UCRL-53745.). The suite contains facilities to
        generate timing statistics and reports."""

    homepage = "https://computing.llnl.gov/projects/co-design/lcals"
    url      = "https://computing.llnl.gov/projects/co-design/download/lcals-v1.0.2.tgz"

    tags = ['proxy-app']

    version('1.0.2', sha256='a146590f7c1e9a9311ccf74dc0bef1fb19d77429db35a33c6725529fb1b0327e')

    variant(
        'microarch',
        description='Micro arch: SSE, AVX, MIC.',
        default='sse',
        values=('sse', 'avx', 'MIC'),
    )

    @property
    def build_targets(self):

        targets = []

        cxxflags = '-std=c++0x '
        cxx_compile = ''

        microarch = self.spec.variants['microarch'].value

        arch = platform.machine()

        if microarch == 'MIC':
            arch = 'MIC'
        elif arch == 'x86_64' or arch == 'x86_32':
            arch = 'x86'
        elif arch != 'bgq':
            raise InstallError('unknown architecture.')

        if self.compiler.name == 'intel':
            if arch == 'MIC':
                cxxflags += '-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_ICC '
                cxx_compile += '-g -O3 -mmic -vec-report3 '
                ' -inline-max-total-size=10000 -inline-forceinline -ansi-alias'
            elif microarch == 'sse' and arch == 'x86':
                cxxflags += '-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_ICC '
                cxx_compile += '-O3 -msse4.1 -inline-max-total-size=10000'
                ' -inline-forceinline -ansi-alias -std=c++0x '
            elif microarch == 'avx' and arch == 'x86':
                cxxflags += '-DLCALS_PLATFORM_X86_AVX -DLCALS_COMPILER_ICC '
                cxx_compile += '-O3 -mavx -inline-max-total-size=10000'
                ' -inline-forceinline -ansi-alias -std=c++0x'
            cxxflags += self.compiler.openmp_flag
        elif self.compiler.name == 'gcc':
            if arch == 'MIC' or (microarch == 'sse' and arch == 'x86'):
                cxxflags += '-DLCALS_PLATFORM_X86_SSE -DLCALS_COMPILER_GNU '
                cxx_compile += '-Ofast -msse4.1 -finline-functions'
                ' -finline-limit=10000 -std=c++11 '
            elif microarch == 'avx' and arch == 'x86':
                cxxflags += '-DLCALS_PLATFORM_X86_AVX -DLCALS_COMPILER_GNU '
                cxx_compile += '-Ofast -mavx -finline-functions'
                ' -finline-limit=10000 -std=c++11'
            elif arch == 'bgq':
                cxxflags += '-DLCALS_PLATFORM_BGQ -DLCALS_COMPILER_GNU '
                cxx_compile += '-O3 -finline-functions -finline-limit=10000'
                ' -std=c++0x'
            cxxflags += self.compiler.openmp_flag
        elif self.compiler.name == 'xl' and arch == 'bgp':
            if self.compiler.version == Version('9') and arch == 'bgp':
                cxxflags += '-DLCALS_PLATFORM_BGP -DLCALS_COMPILER_XLC9 '
                cxx_compile += 'O3 -qarch=450d -qtune=450 -qalias=allp -qhot'
                ' -qsmp=omp '
            elif self.compiler.version == Version('12') and arch == 'bgq':
                cxxflags += '-DLCALS_PLATFORM_BGQ -DLCALS_COMPILER_XLC12 '
                cxx_compile += '-O3 -qarch=qp -qhot=novector -qsimd=auto'
                ' -qlanglvl=extended0x -qnostrict -qinline=10000 -qsmp=omp '
        elif self.compiler.name == 'clang':
            if arch == 'bgq':
                cxxflags += '-DLCALS_PLATFORM_BGQ -DLCALS_COMPILER_CLANG '
                cxx_compile += '-O3 -finline-functions  -ffast-math -std=c++0x'

        targets.append('LCALS_ARCH=')
        cxx_compile += ' ' + cxxflags
        targets.append('CXX_COMPILE={0} {1}'.format(spack_cxx, cxx_compile))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('lcals.exe', prefix.bin)
        install('lcalsversioninfo.txt', prefix)
