# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Poplddecay(MakefilePackage):
    """
    PopLDdecay: a fast and effective tool for linkage disequilibrium
    decay analysis based on variant call format files
    """

    homepage = "https://github.com/BGI-shenzhen/PopLDdecay"
    url      = "https://github.com/BGI-shenzhen/PopLDdecay/archive/v3.41.tar.gz"

    maintainers = ['robqiao']

    version('3.41', sha256='09a1ad01581520b84ef73eaa0b199879c84e77b259ba6ff06dbca5fcfc090457')
    version('3.40', sha256='5070930166fb90f7eaaa4b87c4430caa8a827d79c54683e2f56434a4daf69778')

    def build(self, spec, prefix):
        ###################
        # Build Directory #
        ###################
        with working_dir('src'):
            make()
            make('clean')

    def install(self, spec, prefix):
        mkdirp(prefix.bin.bin)
        install('bin/PopLDdecay', prefix.bin.bin)
        install_tree('bin', prefix.bin)

