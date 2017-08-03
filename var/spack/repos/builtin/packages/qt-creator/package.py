##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os


class QtCreator(Package):
    """The Qt Creator IDE."""
    homepage = 'https://www.qt.io/ide/'
    url      = 'http://download.qt.io/official_releases/qtcreator/4.1/4.1.0/qt-creator-opensource-src-4.1.0.tar.gz'

    list_url = 'http://download.qt.io/official_releases/qtcreator/'
    list_depth = 2

    version('4.1.0',  '657727e4209befa4bf5889dff62d9e0a')

    depends_on("qt")
    depends_on("sqlite@3.8.5")

    def install(self, spec, prefix):
        os.environ['INSTALL_ROOT'] = self.prefix
        qmake = which('qmake')
        qmake('-r')
        make()
        make("install")
