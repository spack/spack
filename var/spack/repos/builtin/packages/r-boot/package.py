# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBoot(RPackage):
    """Functions and datasets for bootstrapping from the book "Bootstrap
    Methods and Their Application" by A. C. Davison and D. V. Hinkley (1997,
    CUP), originally written by Angelo Canty for S."""

    homepage = "https://cran.r-project.org/package=boot"
    url      = "https://cran.r-project.org/src/contrib/boot_1.3-18.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/boot"

    version('1.3-20', 'bb879fb4204a4f94ab82c98dd1ad5eca')
    version('1.3-18', '711dd58af14e1027eb8377d9202e9b6f')
