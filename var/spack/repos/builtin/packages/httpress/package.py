# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Httpress(MakefilePackage):
    """High performance HTTP server stress & benchmark utility"""

    homepage = "https://bitbucket.org/yarosla/httpress/wiki/Home"
    url      = "https://bitbucket.org/yarosla/httpress/get/f27fa1949044.zip"

    def url_for_version(self, version):
        url = "https://bitbucket.org/yarosla/httpress/get/f27fa1949044.zip"
        return url

    version('develop', sha256='fd5503864d201b921b20e7c5f1dce2c013e5215f4cbdf3f32344e9f743e6e964')

    depends_on('libev')
    depends_on('gnutls')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.obj)
        install_tree('./bin/Release', prefix.bin)
        install_tree('./obj/Release', prefix.obj)
