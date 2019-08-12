# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nmap(AutotoolsPackage):
    """Nmap ("Network Mapper") is a free and open source (license)
       utility for network discovery and security auditing.
       It also provides ncat an updated nc"""

    homepage = "https://nmap.org"
    url      = "https://nmap.org/dist/nmap-7.70.tar.bz2"

    version('7.70', '84eb6fbe788e0d4918c2b1e39421bf79')
    version('7.31', 'f2f6660142a777862342a58cc54258ea')
    version('7.30', '8d86797d5c9e56de571f9630c0e6b5f8')
