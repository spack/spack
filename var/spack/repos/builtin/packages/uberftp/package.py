# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Uberftp(AutotoolsPackage):
    """UberFTP is an interactive (text-based) client for GridFTP"""

    homepage = "http://toolkit.globus.org/grid_software/data/uberftp.php"
    url      = "https://github.com/JasonAlt/UberFTP/archive/Version_2_8.tar.gz"

    version('2_8', sha256='8a397d6ef02bb714bb0cbdb259819fc2311f5d36231783cd520d606c97759c2a')
    version('2_7', sha256='29a111a86fa70dbbc529a5d3e5a6befc1681e64e32dc019a1a6a98cd43ffb204')
    version('2_6', sha256='2823a564801fb71d06fe6fbc3a37f11962af75b33c53bf698f26776ec972fe68')

    depends_on('globus-toolkit')
