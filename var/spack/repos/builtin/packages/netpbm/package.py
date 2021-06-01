# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from shutil import copyfile


class Netpbm(MakefilePackage):
    """Netpbm - graphics tools and converters.

    A whole bunch of utilities for primitive manipulation of
    graphic images. Wide array of converters
    from one graphics format to another. E.g.
    from g3 fax format to jpeg. Many basic graphics
    editing tools such as magnifying and cropping.
    """

    homepage = "http://netpbm.sourceforge.net"
    url      = "https://sourceforge.net/projects/netpbm/files/super_stable/10.73.35/netpbm-10.73.35.tgz/download"

    version('10.73.35', sha256='628dbe8490bc43557813d1fedb2720dfdca0b80dd3f2364cb2a45c6ff04b0f18')

    variant('X', default=True,
            description='Enable X libs')

    depends_on('perl', type=('build', 'run'))
    depends_on('gmake', type='build')

    depends_on('zlib')
    depends_on('flex', type='build')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('libpng')

    depends_on('libxi', when='+X')
    depends_on('libxmu', when='+X')
    depends_on('libxt', when='+X')
    depends_on('expat', when='+X')
    depends_on('libx11', when='+X')
    depends_on('pkgconfig', type='build', when='+X')

    def edit(self, spec, prefix):
        # Either run the interactive perl script buildtools/configure.pl
        # or sets the answers directly:
        copyfile('config.mk.in', 'config.mk')
        config = []
        config.append('####Lines above were copied from config.mk.in')
        config.append('DEFAULT_TARGET = nonmerge')
        config.append('LINKER_CAN_DO_EXPLICIT_LIBRARY=Y')
        config.append('LINKERISCOMPILER=Y')
        config.append('NETPBMLIBSUFFIX={0}'.format(dso_suffix))
        config.append('NETPBMLIBTYPE=unixshared')
        config.append('STATICLIB_TOO=Y')
        config.append('LDRELOC = ld --reloc')
        config.append('CC_FOR_BUILD = {0}'.format(self.compiler.cc))
        config.append('LD_FOR_BUILD = {0}'.format(self.compiler.cc))
        config.append('CFLAGS_SHLIB += {0}'.format(self.compiler.cc_pic_flag))

        config.append('TIFFLIB={0}'.format(
            self.spec['libtiff'].libs.ld_flags))
        config.append('TIFFHDR_DIR={0}'.format(
            self.spec['libtiff'].headers.directories[0]))
        config.append('PNGLIB={0}'.format(
            self.spec['libpng'].libs.ld_flags))
        config.append('PNGHDR_DIR={0}'.format(
            self.spec['libpng'].headers.directories[0]))
        config.append('JPEGLIB={0}'.format(
            self.spec['jpeg'].libs.ld_flags))
        config.append('JPEGHDR_DIR={0}'.format(
            self.spec['jpeg'].headers.directories[0]))
        if '+X' in self.spec:
            pkg_config = which('pkg-config')
            if not pkg_config('x11', '--exists'):
                config.append('X11LIB={0}'.format(
                    self.spec['libx11'].libs.ld_flags))
                config.append('X11HDR_DIR={0}'.format(
                    self.spec['libx11'].headers.directories[0]))
        config.append('ZLIB={0}'.format(self.spec['zlib'].libs.ld_flags))
        config.append('NETPBM_DOCURL = http://netpbm.sourceforge.net/doc/')
        config.append('WANT_SSE = Y')
        config.append('MVPROG = mv')
        with open('config.mk', 'a') as mk:
            mk.write('\n'.join(config))

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        bd = join_path(self.build_directory, 'build')
        make('package', 'pkgdir={0}'.format(bd),
             parallel=False)
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        mkdirp(prefix.man)
        # Either run the interactive perl script buildtools/installnetpbm.pl
        # or sets the answers directly:
        with working_dir('build'):
            install_tree("bin", prefix.bin)
            install_tree("lib", prefix.lib)
            install_tree("misc", prefix.lib)
            install_tree("include", prefix.include)
            install_tree(join_path("include", "netpbm"), prefix.include)
            install_tree("man", prefix.man)
