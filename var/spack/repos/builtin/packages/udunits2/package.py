# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Udunits2(AutotoolsPackage):
    """Automated units conversion"""

    homepage = "http://www.unidata.ucar.edu/software/udunits"
    url      = "https://www.gfd-dennou.org/arch/ucar/unidata/pub/udunits/udunits-2.2.24.tar.gz"

    version('2.2.24', '898b90dc1890f172c493406d0f26f531')
    version('2.2.23', '9f66006accecd621a4c3eda4ba9fa7c9')
    version('2.2.21', '1585a5efb2c40c00601abab036a81299')

    depends_on('expat')
