# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Numactl(AutotoolsPackage):
    """NUMA support for Linux"""

    homepage = "http://oss.sgi.com/projects/libnuma/"
    url      = "https://github.com/numactl/numactl/archive/v2.0.11.tar.gz"

    version('2.0.12', sha256='7c3e819c2bdeb883de68bafe88776a01356f7ef565e75ba866c4b49a087c6bdf')
    version('2.0.11', sha256='3e099a59b2c527bcdbddd34e1952ca87462d2cef4c93da9b0bc03f02903f7089')

    patch('numactl-2.0.11-sysmacros.patch', when="@2.0.11")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
