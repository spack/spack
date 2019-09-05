# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Salmon(CMakePackage):
    """Salmon is a tool for quantifying the expression of transcripts using
       RNA-seq data."""

    homepage = "http://combine-lab.github.io/salmon/"
    url      = "https://github.com/COMBINE-lab/salmon/archive/v0.8.2.tar.gz"

    version('0.14.1', sha256='05289170e69b5f291a8403b40d6b9bff54cc38825e9f721c210192b51a19273e')
    version('0.12.0', sha256='91ebd1efc5b0b4c12ec6babecf3c0b79f7102e42b8895ca07c8c8fea869fefa3')
    version('0.9.1', '1277b8ed65d2c6982ed176a496a2a1e3')
    version('0.8.2', 'ee512697bc44b13661a16d4e14cf0a00')

    depends_on('tbb')
    depends_on('boost@:1.66.0')

    depends_on('curl', when='@0.14.1:')

    conflicts('%gcc@:5.1', when='@0.14.1:')

    def patch(self):
        # remove static linking to libstdc++
        filter_file('-static-libstdc++', '', 'CMakeLists.txt', string=True)

    def cmake_args(self):
        args = ['-DBOOST_ROOT=%s' % self.spec['boost'].prefix]
        return args
