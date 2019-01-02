# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Busco(PythonPackage):
    """Assesses genome assembly and annotation completeness with Benchmarking
       Universal Single-Copy Orthologs"""

    homepage = "http://busco.ezlab.org/"
    url      = "https://gitlab.com/api/v4/projects/ezlab%2Fbusco/repository/archive.tar.gz?sha=2.0.1"
    git      = "https://gitlab.com/ezlab/busco.git"

    # TODO: check the installation procedure for version 3.0.2
    # and uncomment the following line
    # version('3.0.2', '31d80042bb7e96422843fa43d0acbd21')

    # There is no tag for version 3.0.1
    version('3.0.1', commit='078252e00399550d7b0e8941cd4d986c8e868a83')
    version('2.0.1', '4dbcc8a0c18fa8f8312c103eb2fbb4e2')

    depends_on('python', type=('build', 'run'))
    depends_on('blast-plus')
    depends_on('hmmer')
    depends_on('augustus')

    def build(self, spec, prefix):
        if self.spec.satisfies('@2.0.1'):
            pass

    def install(self, spec, prefix):
        if self.spec.satisfies('@3.0.1'):
            with working_dir('scripts'):
                mkdirp(prefix.bin)
                install('generate_plot.py', prefix.bin)
                install('run_BUSCO.py', prefix.bin)
            install_tree('config', prefix.config)
            args = self.install_args(spec, prefix)
            self.setup_py('install', *args)
        if self.spec.satisfies('@2.0.1'):
            mkdirp(prefix.bin)
            install('BUSCO.py', prefix.bin)
            install('BUSCO_plot.py', prefix.bin)
