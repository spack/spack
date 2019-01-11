# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Colordiff(Package):
    """Colorful diff utility."""

    homepage = "https://www.colordiff.org"
    url      = "https://www.colordiff.org/colordiff-1.0.18.tar.gz"

    version('1.0.18', '07658f09a44f30a3b5c1cea9c132baed')

    depends_on('perl')

    def install(self, spec, prefix):
        make("INSTALL_DIR=" + prefix.bin, "ETC_DIR=" + prefix.etc,
             "MAN_DIR=" + prefix.man, 'install', parallel=False)
