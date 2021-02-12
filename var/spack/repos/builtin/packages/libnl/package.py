# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Libnl(AutotoolsPackage):
    """libnl - Netlink Protocol Library Suite"""

    homepage = "https://www.infradead.org/~tgr/libnl/"
    url      = "https://github.com/thom311/libnl/releases/download/libnl3_3_0/libnl-3.3.0.tar.gz"

    version('3.5.0', sha256='352133ec9545da76f77e70ccb48c9d7e5324d67f6474744647a7ed382b5e05fa')
    version('3.4.0', sha256='b7287637ae71c6db6f89e1422c995f0407ff2fe50cecd61a312b6a9b0921f5bf')
    version('3.3.0', sha256='705468b5ae4cd1eb099d2d1c476d6a3abe519bc2810becf12fb1e32de1e074e4')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('m4', type='build')

    conflicts('platform=darwin', msg='libnl requires FreeBSD or Linux')
