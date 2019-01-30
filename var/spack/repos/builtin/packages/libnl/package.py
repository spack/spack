# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libnl(AutotoolsPackage):
    """libnl - Netlink Protocol Library Suite"""

    homepage = "https://www.infradead.org/~tgr/libnl/"
    url      = "https://github.com/thom311/libnl/releases/download/libnl3_3_0/libnl-3.3.0.tar.gz"

    version('3.3.0', 'ab3ef137cad95bdda5ff0ffa5175dfa5')
    version('3.2.25', '03f74d0cd5037cadc8cdfa313bbd195c')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('m4', type='build')

    conflicts('platform=darwin', msg='libnl requires FreeBSD or Linux')
