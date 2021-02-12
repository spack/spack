# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XkeyboardConfig(AutotoolsPackage, XorgPackage):
    """This project provides a consistent, well-structured, frequently
    released, open source database of keyboard configuration data. The
    project is targeted to XKB-based systems."""

    homepage = "https://www.freedesktop.org/wiki/Software/XKeyboardConfig/"
    xorg_mirror_path = "data/xkeyboard-config/xkeyboard-config-2.18.tar.gz"

    version('2.31',   sha256='5ac6b5b661aeb9d0ea84ad961cbbdd8fdf2503d6e8ca65ca1b1c5d9aea2ddc52')
    version('2.30',   sha256='105e9cd81999a67001a9e610034a3cb00b7fd3c29b8a32f85c68455b1cc31add')
    version('2.29',   sha256='d8034c8b771b51140409039f8e3351e90a0092238b81af04239794e8d3dc0813')
    version('2.28',   sha256='4424ffaafdf9f09dea69a317709353c4e2b19f69b2405effadce0bac3bdebdff')
    version('2.27',   sha256='eaaa4eef74ca033dacebb1a2fc06a31d7aef3296c236c8ffc55a2f954d7ad448')
    version('2.26',   sha256='8d7e2aaa4e9d66843540e6ef3ebadf79d665d954bfa37d8829be428da6e08bbe')
    version('2.25',   sha256='a777b62b926351c1398e388b61d144c4f0ff2266186d09d7223107d8e96a7bd2')
    version('2.24',   sha256='21276860a413ca351a781732d729b35cdc5800151e7759f1679036b1b16cdd2a')
    version('2.23.1', sha256='6567ccf5d134aae19ef110f5c847d5326aed01fc671167a6b8f8c47aeada0b85')
    version('2.23',   sha256='029dcaf44141849e9f2e8bfc162496e3cda95500b95541f0e2aa0ea2f7896c6d')
    version('2.22',   sha256='17b61ccd0f67ef9354453947cbbbcc87e4abe5b9abc71f7e663066db62d5a22a')
    version('2.21',   sha256='04a1f520fadd1cfa10359dbf5db266b9d7ab11d22194a2afd6116a69776ce4fa')
    version('2.20',   sha256='327ff78eeda1529ff0f1bd1c0962b46de388d5b7e69c8ee5f47e2fddecef6b2a')
    version('2.19',   sha256='f278c3ef6939122e727dab48e06f08916b09e5cfe1837fbfe6b0f69af96a8048')
    version('2.18', sha256='d5c511319a3bd89dc40622a33b51ba41a2c2caad33ee2bfe502363fcc4c3817d')

    depends_on('libx11@1.4.3:')

    depends_on('libxslt', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('intltool@0.30:', type='build')
    depends_on('xproto@7.0.20:')

    # TODO: missing dependencies
    # xgettext
    # msgmerge
    # msgfmt
    # gmsgfmt
    # perl@5.8.1:
    # perl XML::Parser

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XKB_CONFIG_ROOT', self.prefix.share.X11.xkb)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XKB_CONFIG_ROOT', self.prefix.share.X11.xkb)
