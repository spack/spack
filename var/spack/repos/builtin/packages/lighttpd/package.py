# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Lighttpd(CMakePackage):
    """a secure, fast, compliant and very flexible web-server"""

    homepage = "https://www.lighttpd.net"
    url      = "https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.50.tar.gz"

    version('1.4.50', sha256='c9a9f175aca6db22ebebbc47de52c54a99bbd1dce8d61bb75103609a3d798235')
    version('1.4.49', sha256='8b744baf9f29c386fff1a6d2e435491e726cb8d29cfdb1fe20ab782ee2fc2ac7')

    def cmake_args(self):
        return ["-DSBINDIR=bin"]
