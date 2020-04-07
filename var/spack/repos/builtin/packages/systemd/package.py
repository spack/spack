# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Systemd(AutotoolsPackage):
    """systemd is a suite of basic building blocks for a Linux system.
    It provides a system and service manager that runs as PID 1 and
    starts the rest of the system."""

    homepage = "https://github.com/systemd/systemd"
    url      = "https://github.com/systemd/systemd/archive/v245.tar.gz"

    version('245',     sha256='f34f1dc52b2dc60563c2deb6db86d78f6a97bceb29aa0511436844b2fc618040')
    version('244',     sha256='2207ceece44108a04bdd5459aa74413d765a829848109da6f5f836c25aa393aa')
    version('243',     sha256='0611843c2407f8b125b1b7cb93533bdebd4ccf91c99dffa64ec61556a258c7d1')
    version('242',     sha256='ec22be9a5dd94c9640e6348ed8391d1499af8ca2c2f01109198a414cff6c6cba')

    depends_on('gettext')
    depends_on('ninja')
    depends_on('meson')
    depends_on('gperf')
    depends_on('libcap')
    depends_on('util-linux@2.29:+libmount')

    def setup_build_environment(self, env):
        env.append_flags('LDFLAGS', '-L{0} -lintl'.format(
            self.spec['gettext'].prefix.lib))
        env.set('PREFIX', self.prefix)
        env.set('DESTDIR', '/')
