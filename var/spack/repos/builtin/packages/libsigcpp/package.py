# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsigcpp(AutotoolsPackage):
    """Libsigc++ is a C++ library for typesafe callbacks"""

    homepage = "https://libsigcplusplus.github.io/libsigcplusplus/index.html"
    url      = "https://ftp.acc.umu.se/pub/GNOME/sources/libsigc++/2.0/libsigc++-2.0.3.tar.gz"

    version('2.9.3', '0e5630fd0557ee80b5e5cbbcebaa2594')
    version('2.1.1', '5ae4d6da9a408c90e86c776673c38972')
    version('2.0.3', '57c6887dd46ce0bd312a4823589db5d8')

    def url_for_version(self, version):
        """Handle version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/libsigc++"
        ext = '.tar.gz' if version < Version('2.2.10') else '.tar.xz'
        return url + "/%s/libsigc++-%s%s" % (version.up_to(2), version, ext)
