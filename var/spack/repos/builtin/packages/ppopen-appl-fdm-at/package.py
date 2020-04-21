# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PpopenApplFdmAt(MakefilePackage):
    """ppOpen-APPL/FDM with Auto-Tuning"""

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    url      = "file://{0}/ppohFDM_AT_1.0.0.tar.gz".format(os.getcwd())

    version('1.0.0', sha256='f6052b73250a41b2b319b27efc4d753c6ec1f67cd109b53099c2b240f7acd65a')

    depends_on('mpi')
    # depends_on('ppopen-appl-fdm', type='build')

    build_directory = "3.hybrid_AT"
    parallel = False

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            fflags = ['-O3', self.compiler.openmp_flag]
            if spec.satisfies('%gcc'):
                fflags.append('-ffree-line-length-none')
            if spec.satisfies('arch=x86_64:'):
                fflags.append('-mcmodel=medium')
            makefile_opt = FileFilter('Makefile.option')
            makefile_opt.filter(
                'FC = .*$',
                'FC = {0}'.format(spec['mpi'].mpifc)
            )
            makefile_opt.filter(
                'FFLAGS = .*$',
                'FFLAGS = -O3 {0}'.format(' '.join(fflags))
            )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        copy(join_path(self.build_directory, 'seism3d3n'), prefix.bin)
        install_src_dir = join_path(prefix.src, self.build_directory)
        mkdirp(install_src_dir)
        install_tree(self.build_directory, install_src_dir)
        with working_dir(install_src_dir):
            make('clean')
        mkdir(prefix.doc)
        copy('readme.txt', prefix.doc)
