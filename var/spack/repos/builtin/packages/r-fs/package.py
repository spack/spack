# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RFs(RPackage):
    """Cross-Platform File System Operations Based on 'libuv'.

    A cross-platform interface to file system operations, built on top of the
    'libuv' C library."""

    cran = "fs"

    version('1.5.2', sha256='35cad1781d6d17c1feb56adc4607079c6844b63794d0ce1e74bb18dbc11e1987')
    version('1.5.0', sha256='36df1653571de3c628a4f769c4627f6ac53d0f9e4106d9d476afb22ae9603897')
    version('1.3.1', sha256='d6934dca8f835d8173e3fb9fd4d5e2740c8c04348dd2bcc57df1b711facb46bc')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('gmake', type='build')

    depends_on('r-rcpp', type=('build', 'run'), when='@:1.3.1')
