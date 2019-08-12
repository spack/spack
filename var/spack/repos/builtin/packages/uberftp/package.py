# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Uberftp(AutotoolsPackage):
    """UberFTP is an interactive (text-based) client for GridFTP"""

    homepage = "http://toolkit.globus.org/grid_software/data/uberftp.php"
    url      = "https://github.com/JasonAlt/UberFTP/archive/Version_2_8.tar.gz"

    version('2_8', 'bc7a159955a9c4b9f5f42f3d2b8fc830')
    version('2_7', 'faaea2d6e1958c1105cfc9147824e03c')
    version('2_6', '784210976f259f9d19c0798c19778d34')

    depends_on('globus-toolkit')
