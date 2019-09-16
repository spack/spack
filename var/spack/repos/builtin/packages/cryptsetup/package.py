# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cryptsetup(AutotoolsPackage):
    """Cryptsetup and LUKS - open-source disk encryption."""

    homepage = "https://gitlab.com/cryptsetup/cryptsetup"
    url      = "https://www.kernel.org/pub/linux/utils/cryptsetup/v2.2/cryptsetup-2.2.1.tar.xz"
    list_url = "https://www.kernel.org/pub/linux/utils/cryptsetup/"
    list_depth = 1

    version('2.2.1', sha256='94e79a31ed38bdb0acd9af7ccca1605a2ac62ca850ed640202876b1ee11c1c61')

    depends_on('libuuid', type=('build', 'link'))
    depends_on('lvm2', type=('build', 'link'))
    depends_on('popt', type=('build', 'link'))
    depends_on('json-c', type=('build', 'link'))
    depends_on('util-linux~libuuid', type=('build', 'link'))
    depends_on('gettext', type=('build', 'link'))

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # Upstream includes support for discovering the location of the libintl
    # library but is missing the bit in the Makefile.ac that includes it in
    # the LDFLAGS. See https://gitlab.com/cryptsetup/cryptsetup/issues/479
    patch('autotools-libintl.patch')

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/cryptsetup/v{0}/cryptsetup-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = [
            'systemd_tmpfilesdir={0}/tmpfiles.d'.format(self.prefix)
        ]
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Prepend the sbin directory to PATH."""
        spack_env.prepend_path('PATH', self.prefix.sbin)
        run_env.prepend_path('PATH', self.prefix.sbin)
