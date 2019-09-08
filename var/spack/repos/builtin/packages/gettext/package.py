# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gettext(AutotoolsPackage):
    """GNU internationalization (i18n) and localization (l10n) library."""

    homepage = "https://www.gnu.org/software/gettext/"
    url      = "https://ftpmirror.gnu.org/gettext/gettext-0.18.3.tar.gz"

    version('0.20.1', sha256='66415634c6e8c3fa8b71362879ec7575e27da43da562c798a8a2f223e6e47f5c')
    version('0.19.8.1', sha256='ff942af0e438ced4a8b0ea4b0b6e0d6d657157c5e2364de57baa279c1c125c43')
    version('0.19.7', sha256='5386d2a40500295783c6a52121adcf42a25519e2d23675950619c9e69558c23f')
    version('0.18.3', sha256='36f3c1043df803565d4977c1efbd41e1ec0f0301acf5f057984406c34cb9f948')

    # Recommended variants
    variant('curses',   default=True, description='Use libncurses')
    variant('libxml2',  default=True, description='Use libxml2')
    variant('git',      default=True, description='Enable git support')
    variant('tar',      default=True, description='Enable tar support')
    variant('bzip2',    default=True, description='Enable bzip2 support')
    variant('xz',       default=True, description='Enable xz support')

    # Optional variants
    variant('libunistring', default=False, description='Use libunistring')

    # Recommended dependencies
    depends_on('ncurses',  when='+curses')
    depends_on('libxml2',  when='+libxml2')
    # Java runtime and compiler (e.g. GNU gcj or kaffe)
    # C# runtime and compiler (e.g. pnet or mono)
    depends_on('tar',      when='+tar')
    # depends_on('gzip',     when='+gzip')
    depends_on('bzip2',    when='+bzip2')
    depends_on('xz',       when='+xz', type=('build', 'link', 'run'))

    # Optional dependencies
    # depends_on('glib')  # circular dependency?
    # depends_on('libcroco@0.6.1:')
    depends_on('libunistring', when='+libunistring')
    # depends_on('cvs')

    patch('test-verify-parallel-make-check.patch', when='@:0.19.8.1')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--disable-java',
            '--disable-csharp',
            '--with-included-glib',
            '--with-included-gettext',
            '--with-included-libcroco',
            '--without-emacs',
            '--with-lispdir=%s/emacs/site-lisp/gettext' % self.prefix.share,
            '--without-cvs'
        ]

        if '+curses' in spec:
            config_args.append('--with-ncurses-prefix={0}'.format(
                spec['ncurses'].prefix))
        else:
            config_args.append('--disable-curses')

        if '+libxml2' in spec:
            config_args.append('CPPFLAGS=-I{0}/include'.format(
                spec['libxml2'].prefix))
            config_args.append('LDFLAGS=-L{0} -Wl,-rpath,{0}'.format(
                spec['libxml2'].libs.directories[0]))
        else:
            config_args.append('--with-included-libxml')

        if '+bzip2' not in spec:
            config_args.append('--without-bzip2')

        if '+xz' not in spec:
            config_args.append('--without-xz')

        if '+libunistring' in spec:
            config_args.append('--with-libunistring-prefix={0}'.format(
                spec['libunistring'].prefix))
        else:
            config_args.append('--with-included-libunistring')

        return config_args

    @property
    def libs(self):
        return find_libraries(
            ["libasprintf", "libgettextlib", "libgettextpo", "libgettextsrc",
                "libintl"],
            root=self.prefix, recursive=True
        )
