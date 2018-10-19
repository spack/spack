# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PaxUtils(AutotoolsPackage):
    """ELF utils that can check files for security relevant properties"""

    homepage = "https://wiki.gentoo.org/index.php?title=Project:Hardened/PaX_Utilities"
    url      = "https://dev.gentoo.org/~vapier/dist/pax-utils-1.2.2.tar.xz"

    version('1.2.2', 'a580468318f0ff42edf4a8cd314cc942')
