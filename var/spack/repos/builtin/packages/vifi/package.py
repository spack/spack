# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vifi(Package):
    """ViFi is a collection of python and perl scripts
    for identifying viral integration and fusion mRNA reads from NGS data."""

    homepage = "https://github.com/namphuon/ViFi"
    url      = "https://github.com/namphuon/ViFi.git"

    version('master', git='https://github.com/namphuon/ViFi.git', tag='master')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('scripts', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('test', prefix.test)
        install('LICENSE', prefix)
        install('README.md', prefix)
        install('TUTORIAL.md', prefix)
