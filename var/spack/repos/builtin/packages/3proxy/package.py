# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class _3proxy(MakefilePackage):
    """3proxy - tiny free proxy server"""

    homepage = "https://3proxy.org"
    url      = "https://github.com/z3APA3A/3proxy/archive/0.8.13.tar.gz"

    version('0.9.3', sha256='0269095ca0ad91904bf80f7e8774d587464e951ad48a5b9a49d46d0b6bb56ce3')
    version('0.9.2', sha256='b08d85e6c1f68c83ab4bd330c8e9dbb0c0d6bc703e14d88e599c727fed8d2ad9')
    version('0.9.1', sha256='5d118848768836bf91d42858300bf22e0bede3b0f99cf9b3c9a30f9a4e4303ee')
    version('0.9.0', sha256='a58e253354146b24d9e82b1122cc12af252363e6c7a676ca139607fd23b31c37')
    version('0.8.13', sha256='a6d3cf9dd264315fa6ec848f6fe6c9057db005ce4ca8ed1deb00f6e1c3900f88')
    version('0.8.12', sha256='c2ad3798b4f0df06cfcc7b49f658304e451d60e4834e2705ef83ddb85a03f849')
    version('0.8.11', sha256='fc4295e1a462baa61977fcc21747db7861c4e3d0dcca86cbaa3e06017e5c66c9')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def build(self, spec, prefix):
        make('-f', 'Makefile.{0}'.format(platform.system()))

    def install(self, spec, prefix):
        make('-f', 'Makefile.{0}'.format(platform.system()),
             'prefix={0}'.format(prefix), 'install')
