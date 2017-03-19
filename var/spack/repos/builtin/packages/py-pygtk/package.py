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


class PyPygtk(AutotoolsPackage):
    """bindings for the Gtk2 in Python.
       use pygobject for Gtk3."""
    homepage = "http://www.pygtk.org/"
    url      = "http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.gz"

    version('2.24.0', 'd27c7f245a9e027f6b6cd9acb7468e36')

    extends('python')
    depends_on("libffi")
    depends_on('cairo')
    depends_on('glib')
    # for GTK 3.X use pygobject 3.X instead of pygtk
    depends_on('gtkplus+X@2.24:2.99')
    depends_on('py-pygobject@2.28:2.99', type=('build', 'run'))
    depends_on('py-py2cairo', type=('build', 'run'))

    def install(self, spec, prefix):
        make('install', parallel=False)
