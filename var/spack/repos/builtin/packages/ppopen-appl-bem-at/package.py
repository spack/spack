# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PpopenApplBemAt(MakefilePackage):
    """
    ppOpen-APPL/BEM-AT is ppOpen-APPL/Bem with auto tuning.
    If you want to use ppOpen-APPL/BERM-AT, please copy files in
    src/framework_with_template from ppOpen-APPL/BEM install directory.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    url = "file://{0}/ppohBEM_AT_0.1.0.tar.gz".format(os.getcwd())

    version('0.1.0', sha256='215034fea7d9f64e6361d8e605e04c7f5d302c87ce048dcd6d146b14d22c17f9')
    # In OAT_bem-bb-fw-dense-0.1.0.f90 the 2 variables are defined.
    # But ame variables are already defined in include file DAT.h.
    # This patch is deleted the variables definitions
    # in OAT_bem-bb-fw-dense-0.1.0.f90.
    patch('duplicate_defs.patch', when="@0.1.0")

    depends_on('mpi')
    depends_on('ppopen-appl-bem', type='run')

    parallel = False
    build_directory = 'framework_with_templates'
    build_targets = ['SYSTEM=spack']

    def edit(self, spec, prefix):
        flags = ['-O3', self.compiler.openmp_flag]
        fflags = flags[:]
        if spec.satisfies('%gcc'):
            fflags.append('-ffree-line-length-none')
        with open(join_path(self.build_directory, 'Makefile'), 'a') as m:
            m.write('ifeq ($(SYSTEM),spack)\n')
            m.write('    CC = {0}\n'.format(spec['mpi'].mpicc))
            m.write('    F90 = {0}\n'.format(spec['mpi'].mpifc))
            m.write('    CCFLAGS = {0}\n'.format(' '.join(flags)))
            m.write('    F90FLAGS = {0}\n'.format(' '.join(fflags)))
            m.write('    FFLAGS = {0}\n'.format(' '.join(fflags)))
            m.write('    LDFLAGS = {0}\n'.format(' '.join(flags)))
            m.write('endif\n')

    def install(self, spec, prefix):
        install_src_dir = join_path(prefix.src, self.build_directory)
        mkdir(prefix.bin)
        mkdirp(install_src_dir)
        for f in find(self.build_directory, '*.out'):
            copy(f, prefix.bin)
        install_src = join_path(prefix.src, self.build_directory)
        install_tree(self.build_directory, install_src_dir)
        with working_dir(install_src):
            make('clean')
