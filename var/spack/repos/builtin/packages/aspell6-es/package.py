# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Aspell6Es(AspellDictPackage):
    """Spanish (es) dictionary for aspell."""

    homepage = "http://aspell.net/"
    url      = "https://ftpmirror.gnu.org/aspell/dict/es/aspell6-es-1.11-2.tar.bz2"

    version('1.11-2', sha256='ad367fa1e7069c72eb7ae37e4d39c30a44d32a6aa73cedccbd0d06a69018afcc')
