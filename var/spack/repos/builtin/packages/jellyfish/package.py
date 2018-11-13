# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jellyfish(AutotoolsPackage):
    """JELLYFISH is a tool for fast, memory-efficient counting of k-mers in
       DNA."""

    homepage = "http://www.cbcb.umd.edu/software/jellyfish/"
    url      = "https://github.com/gmarcais/Jellyfish/releases/download/v2.2.7/jellyfish-2.2.7.tar.gz"
    list_url = "http://www.cbcb.umd.edu/software/jellyfish/"

    version('2.2.7', 'f741192d9061f28e34cb67c86a1027ab')
    version('1.1.11', 'dc994ea8b0896156500ea8c648f24846',
            url='http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
