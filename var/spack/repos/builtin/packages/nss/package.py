# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nss(MakefilePackage):
    """Network Security Services (NSS) is a set of libraries designed to
    support cross-platform development of security-enabled client and server
    applications. Applications built with NSS can support SSL v3, TLS, PKCS #5,
    PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3 certificates, and other
    security standards."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS"
    url      = "https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_67_RTM/src/nss-3.67.tar.gz"

    version('3.67', sha256='f6549a9148cd27b394b40c77fa73111d5ea23cdb51d796665de1b7458f88ce7f')

    depends_on('nspr@4.24:')
    depends_on('sqlite')
    depends_on('zlib')

    parallel = False

    build_directory = 'nss'

    @property
    def build_targets(self):
        # We cannot use nss_build_all because this will try to build nspr.
        targets = ['all', 'latest']

        targets.append('USE_64=1')
        targets.append('BUILD_OPT=1')

        for var in ('DIST', 'SOURCE_PREFIX', 'SOURCE_MD_DIR'):
            targets.append('{0}={1}'.format(
                var, join_path(self.stage.source_path, 'dist')))

        targets.append('NSS_USE_SYSTEM_SQLITE=1')

        if self.spec.satisfies('%gcc@10:'):
            targets.append('NSS_ENABLE_WERROR=0')

        return targets

    def install(self, spec, prefix):
        install_tree('dist/bin', prefix.bin, symlinks=False)
        install_tree('dist/public/nss', prefix.include.nss, symlinks=False)
        install_tree('dist/lib', prefix.lib, symlinks=False)

    @run_after('install')
    def install_pkgconfig(self):
        pkg_path = join_path(self.prefix.lib, 'pkgconfig')
        mkdirp(pkg_path)

        with open(join_path(pkg_path, 'nss.pc'), 'w') as f:
            f.write('prefix={0}\n'.format(self.prefix))
            f.write('exec_prefix=${prefix}\n')
            f.write('libdir={0}\n'.format(self.prefix.lib))
            f.write('includedir={0}\n'.format(self.prefix.include.nss))
            f.write('\n')
            f.write('Name: NSS\n')
            f.write('Description: Network Security Services\n')
            f.write('Version: {0}\n'.format(self.spec.version))
            f.write('Requires: nspr\n')
            f.write('Cflags: -I${includedir}\n')
            f.write('Libs: -L${libdir} -lssl3 -lsmime3 -lnss3 -lnssutil3\n')
