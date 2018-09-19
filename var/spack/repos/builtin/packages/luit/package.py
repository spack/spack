##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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


class Luit(Package):
    """Luit is a filter that can be run between an arbitrary application and
    a UTF-8 terminal emulator such as xterm.  It will convert application
    output from the locale's encoding into UTF-8, and convert terminal
    input from UTF-8 into the locale's encoding."""

    homepage = "http://cgit.freedesktop.org/xorg/app/luit"
    url      = "https://www.x.org/archive/individual/app/luit-1.1.1.tar.gz"

    version('1.1.1', '04128a52f68c05129f709196819ddad3')

    depends_on('libfontenc')
    depends_on('libx11')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix),
                  # see http://www.linuxquestions.org/questions/linux-from-scratch-13/can't-compile-luit-xorg-applications-4175476308/  # noqa
                  'CFLAGS=-U_XOPEN_SOURCE -D_XOPEN_SOURCE=600')

        make()
        make('install')
