##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Gettext(AutotoolsPackage):
    """GNU internationalization (i18n) and localization (l10n) library."""

    homepage = "https://www.gnu.org/software/gettext/"
    url      = "http://ftpmirror.gnu.org/gettext/gettext-0.19.7.tar.xz"

    version('0.19.8.1', 'df3f5690eaa30fd228537b00cb7b7590')
    version('0.19.7',   'f81e50556da41b44c1d59ac93474dca5')

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
    depends_on('xz',       when='+xz')

    # Optional dependencies
    # depends_on('glib')  # circular dependency?
    # depends_on('libcroco@0.6.1:')
    depends_on('libunistring', when='+libunistring')
    # depends_on('cvs')

    def configure_args(self):
        spec = self.spec

        config_args = [
            '--disable-java',
            '--disable-csharp',
            '--with-included-glib',
            '--with-included-gettext',
            '--with-included-libcroco',
            '--without-emacs',
            '--with-lispdir=%s/emacs/site-lisp/gettext' % prefix.share,
            '--without-cvs'
        ]

        if '+curses' in spec:
            config_args.append('--with-ncurses-prefix={0}'.format(
                spec['ncurses'].prefix))
        else:
            config_args.append('--disable-curses')

        if '+libxml2' in spec:
            config_args.append('--with-libxml2-prefix={0}'.format(
                spec['libxml2'].prefix))
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
