# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Busco(PythonPackage):
    """Assesses genome assembly and annotation completeness with Benchmarking
       Universal Single-Copy Orthologs"""

    homepage = "https://busco.ezlab.org/"
    url = "https://gitlab.com/ezlab/busco/-/archive/5.2.2/busco-5.2.2.tar.gz"
    git = "https://gitlab.com/ezlab/busco.git"

    version('5.2.2', sha256='6da327a21674d354dccebcaaa9594fcb5a3b40d1917b7786c5212920e724229f')
    version('4.1.3', sha256='5231de1778d0af278caf43d10d9958ccc2813f533ba40b8e966fbe6d86cdd3ed')
    version('3.0.1', commit='078252e00399550d7b0e8941cd4d986c8e868a83')
    version('2.0.1', sha256='9298d72fdf24e7f0f1cbf0435f987730b913dc2d6b9b3e6b340e9792e4cdcf93')

    # https://busco.ezlab.org/busco_userguide.html#manual-installation
    depends_on('python@3.3:', when='@4:', type=('build', 'run'))
    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', when='@3:', type='build')
    depends_on('blast-plus')
    depends_on('hmmer')
    depends_on('augustus')
    depends_on('py-biopython', when='@4.1.3', type=('build', 'run'))

    def install(self, spec, prefix):
        if self.spec.satisfies('@5:'):
            super(self, PythonPackage).install(spec, prefix)
        if self.spec.satisfies('@4.1.3'):
            install_tree('bin', prefix.bin)
            install_tree('config', prefix.config)
            super(self, PythonPackage).install(spec, prefix)
        if self.spec.satisfies('@3.0.1'):
            with working_dir('scripts'):
                mkdirp(prefix.bin)
                install('generate_plot.py', prefix.bin)
                install('run_BUSCO.py', prefix.bin)
            install_tree('config', prefix.config)
            super(self, PythonPackage).install(spec, prefix)
        if self.spec.satisfies('@2.0.1'):
            mkdirp(prefix.bin)
            install('BUSCO.py', prefix.bin)
            install('BUSCO_plot.py', prefix.bin)
