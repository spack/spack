# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nano(AutotoolsPackage):
    """Tiny little text editor"""

    homepage = "http://www.nano-editor.org"
    url      = "https://www.nano-editor.org/dist/v2.6/nano-2.6.3.tar.gz"

    version('2.6.3', '1213c7f17916e65afefc95054c1f90f9')
    version('2.6.2', '58568a4b8a33841d774c25f285fc11c1')

    depends_on('ncurses')
