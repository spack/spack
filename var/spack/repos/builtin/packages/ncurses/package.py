# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from glob import glob
from os.path import exists, join
from os import makedirs


class Ncurses(AutotoolsPackage, GNUMirrorPackage):
    """The ncurses (new curses) library is a free software emulation of
    curses in System V Release 4.0, and more. It uses terminfo format,
    supports pads and color and multiple highlights and forms
    characters and function-key mapping, and has all the other
    SYSV-curses enhancements over BSD curses."""

    homepage = "http://invisible-island.net/ncurses/ncurses.html"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "ncurses/ncurses-6.1.tar.gz"

    version('6.2', sha256='30306e0c76e0f9f1f0de987cf1c82a5c21e1ce6568b9227f7da5b71cbea86c9d')
    version('6.1', sha256='aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17')
    version('6.0', sha256='f551c24b30ce8bfb6e96d9f59b42fbea30fa3a6123384172f9e7284bcf647260')
    version('5.9', sha256='9046298fb440324c9d4135ecea7879ffed8546dd1b58e59430ea07a4633f563b')

    variant('symlinks', default=False,
            description='Enables symlinks. Needed on AFS filesystem.')
    variant('termlib', default=True,
            description='Enables termlib needs for gnutls in emacs.')

    depends_on('pkgconfig', type='build')

    patch('patch_gcc_5.txt', when='@6.0%gcc@5.0:')
    patch('sed_pgi.patch',   when='@:6.0')

    def setup_build_environment(self, env):
        env.unset('TERMINFO')

    def flag_handler(self, name, flags):
        if name == 'cflags' or name == 'cxxflags':
            flags.append(self.compiler.pic_flag)

        return (flags, None, None)

    def configure(self, spec, prefix):
        opts = [
            '--disable-stripping',
            '--with-shared',
            '--with-cxx-shared',
            '--enable-overwrite',
            '--without-ada',
            '--enable-pc-files',
            '--with-pkg-config-libdir={0}/lib/pkgconfig'.format(self.prefix)
        ]

        nwide_opts = ['--disable-widec',
                      '--without-manpages',
                      '--without-tests']

        wide_opts = ['--enable-widec',
                     '--without-manpages',
                     '--without-tests']

        if '+symlinks' in self.spec:
            opts.append('--enable-symlinks')

        if '+termlib' in self.spec:
            opts.extend(('--with-termlib',
                         '--enable-termcap',
                         '--enable-getcap',
                         '--enable-tcap-names'))

        prefix = '--prefix={0}'.format(prefix)

        configure = Executable('../configure')

        with working_dir('build_ncurses', create=True):
            configure(prefix, *(opts + nwide_opts))

        with working_dir('build_ncursesw', create=True):
            configure(prefix, *(opts + wide_opts))

    def build(self, spec, prefix):
        with working_dir('build_ncurses'):
            make()
        with working_dir('build_ncursesw'):
            make()

    def install(self, spec, prefix):
        with working_dir('build_ncurses'):
            make('install')
        with working_dir('build_ncursesw'):
            make('install')

        # fix for packages like hstr that use "#include <ncurses/ncurses.h>"
        headers = glob(join(prefix.include, '*'))
        for p_dir in ['ncurses', 'ncursesw']:
            path = join(prefix.include, p_dir)
            if not exists(path):
                makedirs(path)
            for header in headers:
                install(header, path)

    @property
    def libs(self):
        return find_libraries(
            ['libncurses', 'libncursesw'], root=self.prefix, recursive=True)
