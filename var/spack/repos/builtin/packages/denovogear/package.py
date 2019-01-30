# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Denovogear(CMakePackage):
    """DeNovoGear is a software package to detect de novo mutations using
    next-generation sequencing data. It supports the analysis of many
    differential experimental designs and uses advanced statistical models
    to reduce the false positve rate."""

    homepage = "https://github.com/denovogear/denovogear"
    url      = "https://github.com/denovogear/denovogear/archive/v1.1.1.tar.gz"

    version('1.1.1', 'da30e46851c3a774653e57f98fe62e5f')
    version('1.1.0', '7d441d56462efb7ff5d3a6f6bddfd8b9')

    depends_on('cmake@3.1:', type=('build'))
    depends_on('boost@1.47:1.60', type=('build'))
    depends_on('htslib@1.2:', type=('build'))
    depends_on('eigen', type=('build'))
