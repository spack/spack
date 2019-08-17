# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPurrr(RPackage):
    """A complete and consistent functional programming toolkit for R."""

    homepage = "http://purrr.tidyverse.org/"
    url      = "https://cloud.r-project.org/src/contrib/purrr_0.2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/purrr"

    version('0.3.2', sha256='27c74dd9e4f6f14bf442473df22bcafc068822f7f138f0870326532f143a9a31')
    version('0.3.1', sha256='c2a3c9901192efd8a04976676f84885a005db88deb1432e4750900c7b3b7883b')
    version('0.2.4', 'd9a11e6c14771beb3ebe8f4771a552f3')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-rlang@0.3.1:', type=('build', 'run'))
    depends_on('r-tibble', when='@:0.2.9', type=('build', 'run'))
