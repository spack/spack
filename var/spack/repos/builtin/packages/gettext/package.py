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

class Gettext(Package):
    """GNU internationalization (i18n) and localization (l10n) library."""
    homepage = "https://www.gnu.org/software/gettext/"
    url      = "http://ftpmirror.gnu.org/gettext/gettext-0.19.7.tar.xz"

    version('0.19.7', 'f81e50556da41b44c1d59ac93474dca5')

    def install(self, spec, prefix):
        options = ['--disable-dependency-tracking',
                   '--disable-silent-rules',
                   '--disable-debug',
                   '--prefix=%s' % prefix,
                   '--with-included-gettext',
                   '--with-included-glib',
                   '--with-included-libcroco',
                   '--with-included-libunistring',
                   '--with-emacs',
                   '--with-lispdir=%s/emacs/site-lisp/gettext' % prefix.share,
                   '--disable-java',
                   '--disable-csharp',
                   '--without-git', # Don't use VCS systems to create these archives
                   '--without-cvs',
                   '--without-xz']

        configure(*options)

        make()
        make("install")
