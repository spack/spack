# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# TODO: Use gyp/ninja build system to have a faster compilation.

import glob
from os import makedirs

from llnl.util.filesystem import install_tree, join_path, FileFilter, install
from spack.build_systems.makefile import MakefilePackage
from spack.directives import version, variant, depends_on, patch


class Nss(MakefilePackage):
    """Network Security Services (NSS) is a set of libraries designed to support
    cross-platform development of security-enabled client and server
    applications."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS"

    version(
        '3.46.1',
        url=
        "https://ftp.Mozilla.org/pub/security/nss/releases/NSS_3_46_1_RTM/src/nss-3.46.1.tar.gz",
        sha256=
        '3bf7e0ed7db98803f134c527c436cc68415ff17257d34bd75de14e9a09d13651',
        when='~nspr')

    version(
        '3.46.1',
        url=
        "https://ftp.mozilla.org/pub/security/nss/releases/NSS_3_46_1_RTM/src/nss-3.46.1-with-nspr-4.21.tar.gz",
        sha256=
        '5ec5a4e4247eb60b8c15d5151e5b5ce6c14a751e4f2158c9435f498bd5c547f4',
        when='+nspr')

    variant("nspr", default=True, description="Enable internal nspr")

    # Compile instructions from Linux From Scratch:
    # see http://www.linuxfromscratch.org/blfs/view/cvs/postlfs/nss.html
    # patch('nss-3.46.1-standalone-1.patch')
    patch('pkgconfig.patch')

    parallel = False
    depends_on('zlib')
    depends_on('nspr', when='~nspr')
    depends_on('sqlite@3:')

    build_directory = "nss"

    def edit(self, spec, prefix):
        nss_major_version = 3
        nss_minor_version = 46
        nss_patch_version = 1
        nspr_major_version = 4
        nspr_minor_version = 21
        nspr_patch_version = 0

        pkg_filter = FileFilter('pkgconfig/nss.pc', 'pkgconfig/nspr.pc')
        pkg_filter.filter('@prefix@', format(prefix))
        pkg_filter.filter('@exec_prefix@', format(prefix.bin))
        pkg_filter.filter('@libdir@', format(prefix.lib))
        pkg_filter.filter('@includedir@', format(prefix.include))
        pkg_filter.filter('@NSS_MAJOR_VERSION@', format(nss_major_version))
        pkg_filter.filter('@NSS_MINOR_VERSION@', format(nss_minor_version))
        pkg_filter.filter('@NSS_PATCH_VERSION@', format(nss_patch_version))
        pkg_filter.filter('@NSPR_MAJOR_VERSION@', format(nspr_major_version))
        pkg_filter.filter('@NSPR_MINOR_VERSION@', format(nspr_minor_version))
        pkg_filter.filter('@NSPR_PATCH_VERSION@', format(nspr_patch_version))
        pkg_filter.filter(
            '@NSPR_MIN_VERSION@', '{}.{}'.format(nspr_major_version,
                                                 nspr_minor_version))

    @property
    def build_targets(self):
        args = [
            'nss_build_all', 'USE_SYSTEM_ZLIB=1', 'NSS_ENABLE_WERROR=0',
            'USE_64=1', 'BUILD_OPT=1'
        ]
        args.append('NSS_USE_SYSTEM_SQLITE=1')
        if self.spec.satisfies('~nspr'):
            args.append('NSPR_INCLUDE_DIR={}/nspr'.format(
                self.spec['nspr'].prefix.include))
        return args

    def install(self, spec, prefix):
        for d in [prefix.bin, prefix.lib, prefix.include]:
            try:
                makedirs(d)
            except FileExistsError:
                pass
        base_path = 'dist'
        install_tree(join_path(base_path, 'public/dbm'),
                     prefix.include,
                     symlinks=False)
        install_tree(join_path(base_path, 'public/nss'),
                     prefix.include,
                     symlinks=False)
        compile_dir = glob.glob(join_path(base_path, '*.OBJ'))[0]
        install_tree(join_path(compile_dir, 'include'),
                     prefix.include,
                     symlinks=False)
        install_tree(join_path(compile_dir, 'lib'), prefix.lib, symlinks=False)
        install_tree(join_path(compile_dir, 'bin'), prefix.bin, symlinks=False)
        pkgconfig_dir = join_path(prefix.lib, 'pkgconfig')
        makedirs(pkgconfig_dir)
        install('pkgconfig/nss.pc', pkgconfig_dir)
        if spec.satisfies('+nspr'):
            install('pkgconfig/nspr.pc', pkgconfig_dir)
