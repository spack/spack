# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FlattenDeps(Package):
    """Example install that flattens dependencies."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dependency-install')

    # While the "spack.package." preface is unnecessary, it is specified
    # here to ensure code coverage recognizes the test.
    install = spack.package.install_dependency_symlinks
