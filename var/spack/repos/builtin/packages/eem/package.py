# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eem(MakefilePackage):
    """EEM is a program to extract the gene group and expression modules
       that are co-expressed in the mRNA expression data."""

    homepage = "http://www.scls.riken.jp/scruise/software/eem.html"
    url      = "http://www.scls.riken.jp/wp-content/uploads/2014/07/eemParallel_1.0.1.tar.gz"

    version('1.0.1', sha256='f617ea7350fce3b2581c814f70bda4427cbab83aac54a2dcadb36e8193f300bb')

    variant('K', default=False, description='Build for K computer')

    phases = ['edit', 'install']

    depends_on('mpi')

    build_directory = 'src'

    patch('add_include.patch')
    patch('fix_CXXFLAGS_for_K.patch', when='+K')

    def edit(self, spec, prefix):
        filter_file('$(HOME)/local', '{0}'.format(prefix),
                    './src/local_settings.mk', string=True)
        filter_file('mpicxx', '{0}'.format(self.spec['mpi'].mpicxx),
                    './src/local_settings.mk', string=True)
