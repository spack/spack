# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Diffutils(AutotoolsPackage):
    """GNU Diffutils is a package of several programs related to finding
    differences between files."""

    homepage = "https://www.gnu.org/software/diffutils/"
    url      = "https://ftp.gnu.org/gnu/diffutils/diffutils-3.6.tar.xz"

    version('3.6', sha256='d621e8bdd4b573918c8145f7ae61817d1be9deb4c8d2328a65cea8e11d783bd6')

    build_directory = 'spack-build'
