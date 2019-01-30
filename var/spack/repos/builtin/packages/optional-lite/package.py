# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from shutil import copytree


class OptionalLite(Package):
    """
    A single-file header-only version of a C++17-like optional, a nullable
    object for C++98, C++11 and later.
    """

    homepage = "https://github.com/martinmoene/optional-lite"
    url      = "https://github.com/martinmoene/optional-lite/archive/v3.0.0.tar.gz"

    version('3.0.0', sha256='36ae58512c478610647978811f0f4dbe105880372bd7ed39417314d50a27254e')
    version('2.3.0', sha256='8fe46216147234b172c6a5b182726834afc44dfdca1e976a264d6f96eb183916')
    version('2.2.0', sha256='9ce1bb021de42f804f8d17ed30b79fc98296122bec8db60492104978cd282fa2')
    version('2.0.0', sha256='e8d803cbc7be241df41a9ab267b525b7941df09747cd5a7deb55f863bd8a4e8d')
    version('1.0.3', sha256='7a2fb0fe20d61d091f6730237add9bab58bc0df1288cb96f3e8a61b859539067')

    def install(self, spec, prefix):
        copytree('include', prefix.include)
