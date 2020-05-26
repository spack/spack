# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Quicksilver(MakefilePackage):
    """Quicksilver is a proxy application that represents some elements of the
       Mercury workload.
    """

    tags = ['proxy-app']

    homepage = "https://codesign.llnl.gov/quicksilver.php"
    url      = "https://github.com/LLNL/Quicksilver"
    git      = "https://github.com/LLNL/Quicksilver.git"

    maintainers = ['richards12']

    version('develop', branch='master')

    build_directory = 'src'

    @property
    def build_targets(self):
        targets = []
        targets.append('CXX={0}'.format(spack_cxx))
        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install("src/qs", prefix.bin)
        install('LICENSE.md', prefix.doc)
        install('README.md', prefix.doc)
