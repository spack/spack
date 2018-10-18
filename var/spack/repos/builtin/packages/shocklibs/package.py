# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Shocklibs(Package):
    """The lib for shock: An object store for scientific data."""

    homepage = "https://github.com/MG-RAST/Shock"
    url      = "https://github.com/MG-RAST/Shock/archive/v0.9.24.tar.gz"

    version('0.9.24', '98b2e91e2726c7165f75afaf0ca51a5b')

    def install(self, spec, prefix):
        install_tree('libs', prefix.libs)
