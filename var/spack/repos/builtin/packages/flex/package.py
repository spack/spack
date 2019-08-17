# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"

    version('2.6.4', '2882e3179748cc9f9c23ec593d6adc8d')
    version('2.6.3', 'a5f65570cd9107ec8a8ec88f17b31bb1')
    # Avoid flex '2.6.2' (major bug)
    # See issue #2554; https://github.com/westes/flex/issues/113
    version('2.6.1', '05bcd8fb629e0ae130311e8a6106fa82')
    version('2.6.0', '760be2ee9433e822b6eb65318311c19d')
    version('2.5.39', '5865e76ac69c05699f476515592750d7')

    variant('lex', default=True,
            description="Provide symlinks for lex and libl")

    depends_on('bison',         type='build')
    depends_on('gettext@0.19:', type='build')
    depends_on('help2man',      type='build')

    # Older tarballs don't come with a configure script and the patch for
    # 2.6.4 touches configure
    depends_on('m4',       type='build')
    depends_on('autoconf', type='build', when='@:2.6.0,2.6.4')
    depends_on('automake', type='build', when='@:2.6.0,2.6.4')
    depends_on('libtool',  type='build', when='@:2.6.0,2.6.4')

    # 2.6.4 fails to compile with newer versions of gcc/glibc, see:
    # - https://github.com/spack/spack/issues/8152
    # - https://github.com/spack/spack/issues/6942
    # - https://github.com/westes/flex/issues/241
    patch('https://github.com/westes/flex/commit/24fd0551333e7eded87b64dd36062da3df2f6380.patch', sha256='09c22e5c6fef327d3e48eb23f0d610dcd3a35ab9207f12e0f875701c677978d3', when='@2.6.4')

    @property
    def force_autoreconf(self):
        # The patch for 2.6.4 touches configure
        return self.spec.satisfies('@2.6.4')

    def url_for_version(self, version):
        url = "https://github.com/westes/flex"
        if version >= Version('2.6.1'):
            url += "/releases/download/v{0}/flex-{0}.tar.gz".format(version)
        elif version == Version('2.6.0'):
            url += "/archive/v{0}.tar.gz".format(version)
        elif version >= Version('2.5.37'):
            url += "/archive/flex-{0}.tar.gz".format(version)
        else:
            url += "/archive/flex-{0}.tar.gz".format(version.dashed)

        return url

    @run_after('install')
    def symlink_lex(self):
        """Install symlinks for lex compatibility."""
        if self.spec.satisfies('+lex'):
            dso = dso_suffix
            for dir, flex, lex in \
                    ((self.prefix.bin,   'flex', 'lex'),
                     (self.prefix.lib,   'libfl.a', 'libl.a'),
                     (self.prefix.lib,   'libfl.' + dso, 'libl.' + dso),
                     (self.prefix.lib64, 'libfl.a', 'libl.a'),
                     (self.prefix.lib64, 'libfl.' + dso, 'libl.' + dso)):

                if os.path.isdir(dir):
                    with working_dir(dir):
                        if (os.path.isfile(flex) and not os.path.lexists(lex)):
                            symlink(flex, lex)
