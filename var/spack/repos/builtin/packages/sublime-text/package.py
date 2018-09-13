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


class SublimeText(Package):
    """Sublime Text is a sophisticated text editor for code, markup and
    prose."""

    homepage = "http://www.sublimetext.com/"
    url      = "https://download.sublimetext.com/sublime_text_3_build_3176_x64.tar.bz2"

    version('3_build_3176', '7d4c8c5167224888d901e8cbafb6ec7f')
    version('3_build_3126', 'acc34252b0ea7dff1f581c5db1564dcb')
    version('2.0.2',        '699cd26d7fe0bada29eb1b2cd7b50e4b')

    # Sublime text comes as a pre-compiled binary.
    # Since we can't link to Spack packages, we'll just have to
    # add them as runtime dependencies.

    # depends_on('libgobject', type='run')
    depends_on('glib', type='run')
    depends_on('libx11', type='run')
    depends_on('pcre', type='run')
    depends_on('libffi', type='run')
    depends_on('libxcb', type='run')
    depends_on('libxau', type='run')

    def url_for_version(self, version):
        if version[0] == 2:
            return "https://download.sublimetext.com/Sublime%20Text%20{0}%20x64.tar.bz2".format(version)
        else:
            return "https://download.sublimetext.com/sublime_text_{0}_x64.tar.bz2".format(version)

    def install(self, spec, prefix):
        # Sublime text comes as a pre-compiled binary.
        install_tree('.', prefix)
