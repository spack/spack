# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPacman(RPackage):
    """Tools to more conveniently perform tasks associated with add-on
    packages. pacman conveniently wraps library and package related functions
    and names them in an intuitive and consistent fashion. It seeks to combine
    functionality from lower level functions which can speed up workflow."""

    homepage = "https://cran.r-project.org/package=pacman"
    url      = "https://cran.r-project.org/src/contrib/pacman_0.4.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pacman"

    version('0.4.1', 'bf18fe6d1407d31e00b337d9b07fb648')

    depends_on('r@3.0.2:')

    depends_on('r-devtools', type=('build', 'run'))
