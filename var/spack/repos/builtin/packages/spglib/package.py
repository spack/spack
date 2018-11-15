# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spglib(CMakePackage):
    """C library for finding and handling crystal symmetries."""

    homepage = "https://atztogo.github.io/spglib/"
    url      = "https://github.com/atztogo/spglib/archive/v1.10.3.tar.gz"

    patch('fix_cmake_install.patch', when='@:1.10.3')
    # patch by Krishnendu Ghosh
    patch('fix_cpp.patch', when='@:1.10.3')

    version('1.10.3', 'f6ef0554fa528ffa49d8eaee18a2b7b9')
    version('1.10.0', '0ad9330ae8a511d25e2e26cb9bf02808')
