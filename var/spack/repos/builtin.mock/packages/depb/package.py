# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Depb(Package):
    """Simple package serving as a second package dependent on B"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/depb-1.0.tar.gz"

    version('1.0', '1.0_depb_hash')

    depends_on('b')
