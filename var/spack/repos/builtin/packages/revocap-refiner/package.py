# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RevocapRefiner(MakefilePackage):
    """The University of Tokyo, CISS Project:
        Geometric processing, mesh processing, mesh generation"""

    homepage = "https://github.com/FrontISTR/REVOCAP_Refiner"
    git      = "https://github.com/FrontISTR/REVOCAP_Refiner.git"

    version('master', branch='master')

    depends_on('ruby', type='build')
    depends_on('mpi')
    depends_on('doxygen', type='build')
    depends_on('swig', type='build')

    parallel = False

    def edit(self, spec, prefix):
        cflags = ['-O']
        cxxflags = ['-O',  self.compiler.cxx_pic_flag]
        fflags = ['']
        ldshare = ['']
        libs = ['-lstdc++']
        if spec.satisfies('%gcc'):
            ldshare.append('g++ -shared -s')

        m = FileFilter('MakefileConfig.in')
        m.filter(r'CC\s=.*$', 'CC={0}'.format(spec['mpi'].mpicc))
        m.filter(r'CFLAGS\s=.*$', 'CFLAGS={0}'.format(' '.join(cflags)))
        m.filter(r'CXX\s*=.*$',  'CXX={0}'.format(spec['mpi'].mpicxx))
        m.filter(r'CXXFLAGS\s*=.*$',
                 'CXXFLAGS={0}'.format(' '.join(cxxflags)))
        m.filter(r'AR\s*=.*$', 'AR=ar')
        m.filter(r'ARFLAGS\s*=.*$', 'ARFLAGS=rsv')
        m.filter(r'LD\s*=.*$', 'LD={0}'.format(spack_fc))
        m.filter(r'LDFLAGS\s*=.*$',
                 'LDFLAGS={0}'.format(' '.join(fflags)))
        m.filter(r'LDSHARE\s*=.*$',
                 'LDSHARE={0}'.format(' '.join(ldshare)))
        m.filter(r'LIBS\s*=.*$', 'LIBS={0}'.format(' '.join(libs)))
        m.filter(r'LIBPATH\s*=.*$', 'LIBPATH= ')
        m.filter(r'RM\s*=.*$', 'RM=rm -f')
        m.filter(r'DOXYGEN\s*=.*$', 'DOXYGEN=doxygen')
        m.filter(r'TAR\s*=.*$', 'TAR=tar')
        m.filter(r'SWIG\s*=.*$', 'SWIG=swig')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('Refiner',  prefix.include.refine)
