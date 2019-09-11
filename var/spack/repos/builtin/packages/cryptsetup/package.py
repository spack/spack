# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cryptsetup(AutotoolsPackage):
    """Cryptsetup and LUKS - open-source disk encryption."""

    homepage = "https://gitlab.com/cryptsetup/cryptsetup"
    url      = "https://www.kernel.org/pub/linux/utils/cryptsetup/v2.2/cryptsetup-2.2.1.tar.xz"

    version('2.2.1', sha256='94e79a31ed38bdb0acd9af7ccca1605a2ac62ca850ed640202876b1ee11c1c61')

    depends_on('libuuid', type=('build', 'link'))
    depends_on('lvm2', type=('build', 'link'))
    depends_on('popt', type=('build', 'link'))
    depends_on('json-c', type=('build', 'link'))
    depends_on('util-linux', type=('build', 'link'))
    depends_on('gettext', type=('build', 'link'))

    def configure_args(self):
        args = [
            'LIBS=-lintl',
            'systemd_tmpfilesdir={0}/tmpfiles.d'.format(self.prefix)
        ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Prepend the sbin directory to PATH."""
        spack_env.prepend_path('PATH', self.prefix.sbin)
        run_env.prepend_path('PATH', join_path(self.prefix, 'sbin'))
