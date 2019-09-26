# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBoot(RPackage):
    """Functions and datasets for bootstrapping from the book "Bootstrap
    Methods and Their Application" by A. C. Davison and D. V. Hinkley (1997,
    CUP), originally written by Angelo Canty for S."""

    homepage = "https://cloud.r-project.org/package=boot"
    url      = "https://cloud.r-project.org/src/contrib/boot_1.3-18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/boot"

    version('1.3-23', sha256='30c89e19dd6490b943233e87dfe422bfef92cfbb7a7dfb5c17dfd9b2d63fa02f')
    version('1.3-22', sha256='cf1f0cb1e0a7a36dcb6ae038f5d0211a0e7a009c149bc9d21acb9c58c38b4dfc')
    version('1.3-20', 'bb879fb4204a4f94ab82c98dd1ad5eca')
    version('1.3-18', '711dd58af14e1027eb8377d9202e9b6f')

    depends_on('r@3.0.0:', type=('build', 'run'))
