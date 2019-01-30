# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Salmon(CMakePackage):
    """Salmon is a tool for quantifying the expression of transcripts using
       RNA-seq data."""

    homepage = "http://combine-lab.github.io/salmon/"
    url      = "https://github.com/COMBINE-lab/salmon/archive/v0.8.2.tar.gz"

    version('0.9.1', '1277b8ed65d2c6982ed176a496a2a1e3')
    version('0.8.2', 'ee512697bc44b13661a16d4e14cf0a00')

    depends_on('tbb')
    depends_on('boost@:1.66.0')

    def patch(self):
        # remove static linking to libstdc++
        filter_file('-static-libstdc++', '', 'CMakeLists.txt', string=True)

    def cmake_args(self):
        args = ['-DBOOST_ROOT=%s' % self.spec['boost'].prefix]
        return args
