# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvori(CMakePackage):
    """Support for Voronoi Integration and lossless BQB compression"""

    homepage = "https://brehm-research.de/voronoi.php"
    url      = "https://www.cp2k.org/static/downloads/libvori-201217.tar.gz"

    maintainers = ['dev-zero']

    version('201217', sha256='6ad456ed6ca5d28cadcc0d90eabe8fff5caa77b99f12764323de5e3ae21cddf5')
