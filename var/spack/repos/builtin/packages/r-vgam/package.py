# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVgam(RPackage):
    """An implementation of about 6 major classes of statistical regression
    models."""

    homepage = "https://cloud.r-project.org/package=VGAM"
    url      = "https://cloud.r-project.org/src/contrib/VGAM_1.0-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/VGAM"

    version('1.1-1', sha256='de192bd65a7e8818728008de8e60e6dd3b61a13616c887a43e0ccc8147c7da52')
    version('1.0-6', sha256='121820a167411e847b41bdcb0028b55842d0ccc0c3471755c67449837e0fe3b9')
    version('1.0-4', '9d30736842db6d9dcec83df49f11d3c1')
    version('1.0-3', 'a158cd0a6ff956b4bf21d610df361b18')
    version('1.0-2', '813b303d5d956914cf8910db3fa1ba14')
    version('1.0-1', '778182585c774036ac3d10240cf63b40')
    version('1.0-0', '81da7b3a797b5e26b9e859dc2f373b7b')

    depends_on('r@3.0.0:', when='@:1.0-1', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.0-2:1.0-3', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@1.0-4:', type=('build', 'run'))
