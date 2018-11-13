# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pslib(AutotoolsPackage):
    """C-library to create PostScript files on the fly."""

    homepage = "http://pslib.sourceforge.net/"
    url      = "https://kent.dl.sourceforge.net/project/pslib/pslib/0.4.5/pslib-0.4.5.tar.gz"

    version('0.4.5', '03f39393628a6d758799b9f845047e27')

    depends_on('jpeg')
    depends_on('libpng')
