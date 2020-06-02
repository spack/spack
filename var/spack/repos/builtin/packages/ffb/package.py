# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Ffb(Package):
    """Computational Fluid Dynamics Software for aeroacoustics"""

    homepage = "http://www.ciss.iis.u-tokyo.ac.jp/dl/index.php"
    url      = "file://{0}/FrontFlow_blue.8.1.tar.gz".format(os.getcwd())
    version('8.1', sha256='1ad008c909152b6c27668bafbad820da3e6ec3309c7e858ddb785f0a3d6e43ae')

    patch('revocap_refiner.patch')

    depends_on('mpi')
    depends_on('blas')
    depends_on('scalapack')

    parallel = False

    def install(self, spec, prefix):
        d = find('.', 'make', recursive=True)
        workdir = os.path.dirname(d[0])
        POPT = ['-P -traditional-cpp -Dcputime']
        COPT = ['-O3 ']
        FOPT = ['']
        cflags = ['-O']
        cxxflags = ['-O',  self.compiler.cxx_pic_flag]
        fflags = ['']
        ldshared = ['']
        libs = ['-lstdc++']
        INCDIR = spec['mpi'].headers.directories[0]
        LIBDIR = spec['mpi'].libs.directories[0]
        if spec.satisfies('%gcc'):
            FOPT = ['-C ']
            ldshared = ['g++ -shared -s']
            FOPT.append('-mcmodel=large')
        if spec.satisfies('%intel'):
            COPT = ['']
            FOPT.append('-convert big_endian -mcmodel=large -shared-intel')
            cflags = ['-O2']
            cxxflags = ['-O2',  self.compiler.cxx_pic_flag]
            fflags = ['-O2']

        make = join_path(workdir, 'make', 'makefile')
        m = FileFilter(make)
        m.filter(
            r'#LES3DHOME   =', 'LES3DHOME= {0}\n'.format(workdir))
        m.filter(r'OPTION\n', 'OPTION.spack')
        with open(join_path(workdir, 'make', 'OPTION.spack'), 'w') as m:
            m.write('CPP = /lib/cpp\n')
            m.write('CCOM = {0}\n'.format(spack_cc))
            m.write('POPT = {0}\n'.format(' '.join(POPT)))
            m.write('COPT = {0}\n'.format(' '.join(COPT)))
            m.write('FCOM = {0}\n'.format(spack_fc))
            m.write('FOPT = {0}\n'.format(' '.join(FOPT)))
            m.write('INCDIR = {0}\n'.format(INCDIR))
            m.write('LIBDIR = {0}\n'.format(LIBDIR))

        # for MPI
        with open(join_path(workdir, 'make', 'OPTION'), 'w') as m:
            m.write('CPP = /lib/cpp\n')
            m.write('CCOM = {0}\n'.format(spec['mpi'].mpicc))
            m.write('POPT = {0}\n'.format(' '.join(POPT)))
            m.write('COPT = {0}\n'.format(' '.join(COPT)))
            m.write('FCOM = {0}\n'.format(spec['mpi'].mpifc))
            m.write('FOPT = {0}\n'.format(' '.join(FOPT)))
            m.write('INCDIR = {0}\n'.format(INCDIR))
            m.write('LIBDIR = {0}\n'.format(LIBDIR))

        srcdir = join_path(workdir, 'lib', 'src')
        utildir = join_path(workdir, 'util')
        with open(join_path(workdir, 'make', 'Makeall'), 'w') as m:
            m.write('#!/bin/csh -f\n')
            m.write('setenv LES3DHOME {0}\n'.format(workdir))
            m.write('cd {0}\n'.format(srcdir))
            m.write('./Makeall\n')
            m.write('cd {0}\n'.format(utildir))
            m.write('./Makeall\n')

        Makeall = join_path(workdir, 'lib', 'src', 'dd_mpi', 'Makeall')
        dd_mpi_dir = join_path(workdir, 'lib', 'src', 'dd_mpi')
        with open(Makeall, 'w') as m:
            m.write('#!/bin/csh -f\n')
            m.write('setenv LES3DHOME {0}\n'.format(''.join(workdir)))
            m.write('cd {0}\n'.format(dd_mpi_dir))
            m.write('make lib\n')
        os.chmod(Makeall, 0o755)

        Makeall = join_path(workdir, 'util',  'makeall')
        les3d_dir = join_path(workdir, 'util', 'les3d.mpi')
        les3c_dir = join_path(workdir, 'util', 'les3c.mpi')
        les3ct_dir = join_path(workdir, 'util', 'les3ct.mpi')
        les3x_dir = join_path(workdir, 'util', 'les3x.mpi')
        with open(Makeall, 'w') as m:
            m.write('#!/bin/csh -f\n')
            m.write('setenv LES3DHOME {0}\n'.format(''.join(workdir)))
            m.write('cd {0}\n'.format(les3d_dir))
            m.write('make\n')
            m.write('cd {0}\n'.format(les3c_dir))
            m.write('make\n')
            m.write('cd {0}\n'.format(les3ct_dir))
            m.write('make\n')
            m.write('cd {0}\n'.format(les3x_dir))
            m.write('make\n')
            for d in [les3c_dir, les3ct_dir, les3d_dir]:
                editfile = join_path(d, 'FILES')
                m = FileFilter(editfile)
                m.filter(r'-lmpi_f77', '')
        os.chmod(Makeall, 0o755)

        editfile = join_path(workdir, 'lib', 'src',
                             'REVOCAP_Refiner-0.4.3', 'OPTIONS')
        m = FileFilter(editfile)
        m.filter(r'ARCH\s*=.*$', 'ARCH=`arch`-linux')
        m.filter(r'CC\s*=.*$', 'CC={0}'.format(spack_cc))
        m.filter(r'CFLAGS\s*=.*$', 'CFLAGS={0}'.format(' '.join(cflags)))
        m.filter(r'CXX\s*=.*$',  'CXX={0}'.format(spack_cxx))
        m.filter(r'CXXFLAGS\s*=.*$',
                 'CXXFLAGS={0}'.format(' '.join(cxxflags)))
        m.filter(r'F90\s*=.*$', 'CC={0}'.format(spack_fc))
        m.filter(r'FFLAGS\s*=.*$', 'FFLAGS={0}'.format(' '.join(cflags)))
        m.filter(r'LD\s*=.*$', 'LD={0}'.format(spack_fc))
        m.filter(r'LDFLAGS\s*=.*$',
                 'LDFLAGS={0}'.format(' '.join(fflags)))
        m.filter(r'LDSHARED\s*=.*$',
                 'LDSHARED={0}'.format(' '.join(ldshared)))
        m.filter(r'LIBS\s*=.*$', 'LIBS={0}'.format(' '.join(libs)))
        m.filter(r'LIBPATH\s*=.*$', 'LIBPATH= ')

        editfile = join_path(workdir, 'util', 'xvx2gf', 'Makefile')
        m = FileFilter(editfile)
        m.filter(
            r'#LES3DHOME   =', 'LES3DHOME= {0}\n'.format(workdir))
        m.filter(r'g\+\+', (spack_cxx))

        editfile = join_path(workdir, 'util', 'les3x.mpi', 'FILES')
        m = FileFilter(editfile)
        m.filter(r'LIBS = -lfort -lgf2 -ldd_mpi -lmpi_f77',
                 'LIBS = -lfort -lgf2  -ldd_mpi')

        makeall = Executable(join_path(workdir, 'make',  'Makeall'))
        makeall()

        make = join_path(workdir, 'make', 'makefile')
        m = FileFilter(make)
        m.filter(r'OPTION.spack', 'OPTION\n')
        makeall = Executable(join_path(workdir,
                             'lib',  'src', 'dd_mpi', 'Makeall'))
        makeall()

        makeall = Executable(join_path(workdir, 'util', 'makeall'))
        makeall()

        install_tree(join_path(workdir, 'bin'), prefix.bin)
        install_tree(join_path(workdir, 'macro'), prefix.macro)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', prefix.macro)
