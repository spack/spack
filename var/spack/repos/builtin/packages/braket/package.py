# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Braket(MakefilePackage):
    """braket is a tool for simulations of quantum gates on (classical) computers. It contains an interpreter of "quantum assembler" bra and a C++ template library ket."""

    homepage = "https://github.com/naoki-yoshioka/braket"
    git = "https://github.com/naoki-yoshioka/braket.git"
    maintainers = ['naoki-yoshioka']

    version('master', branch='master', submodules=True)
    version('1.6.0', tag='v1.6.0', submodules=True)

    variant('mpi', default=True, description='Enables MPI support')
    variant(
        "build",
        default="release",
        description="Build in release mode or debug mode",
        values=("release", "debug"),
        multi=False,
    )
    variant(
        "fp",
        default="double",
        description="Floating point mode uses single or double or long-double",
        values=("single", "double", "long-double"),
        multi=False,
    )    

    depends_on('boost', type=("build", "link"))
    depends_on('mpi', when="+mpi", type=("build", "run"))

    build_directory = 'bra'

    def edit(self, spec, prefix):
        makefile = FileFilter('bra/Makefile')
        if spec.satisfies("%fj"):
           if '~mpi' in self.spec:
               makefile.filter('g\+\+', 'FCC')
           else:
               makefile.filter('mpiCC', 'mpiFCC')

        else:
           if '~mpi' in self.spec:
              makefile.filter('FCCpx', 'g++')
           else:
              makefile.filter('mpiFCCpx', 'mpicxx')
              makefile.filter('mpiCC', 'mpicxx')

           makefile.filter('-Nclang', '')

    @property
    def build_targets(self):
        args = []
        build = self.spec.variants["build"].value
        fp = self.spec.variants["fp"].value
        if '+mpi' in self.spec:
           if 'release' in build:
               if 'single' in fp:
                  args = ['release-float']
               elif 'double' in fp:
                  args = ['release']
               elif 'long-double' in fp:
                  args = ['release-long']
           elif 'debug' in build:
               if 'single' in fp:
                  args = ['debug-float']
               elif 'double' in fp:
                  args = ['debug']
               elif 'long-double' in fp:
                  args = ['debug-long']
        else:
           if 'release' in build:
               if 'single' in fp:
                  args = ['nompi-release-float']
               elif 'double' in fp:
                  args = ['nompi-release']
               elif 'long-double' in fp:
                  args = ['nompi-release-long']
           elif 'debug' in build:
               if 'single' in fp:
                  args = ['nompi-debug-float']
               elif 'double' in fp:
                  args = ['nompi-debug']
               elif 'long-double' in fp:
                  args = ['nompi-debug-long']

        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('bra/bin/bra', prefix.bin)
