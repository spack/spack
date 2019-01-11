# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tclap(AutotoolsPackage):
    """Templatized C++ Command Line Parser"""

    homepage = "http://tclap.sourceforge.net"
    url      = "https://downloads.sourceforge.net/project/tclap/tclap-1.2.2.tar.gz"

    version('1.2.2', '6f35665814dca292eceda007d7e13bcb')
    version('1.2.1', 'eb0521d029bf3b1cc0dcaa7e42abf82a')
