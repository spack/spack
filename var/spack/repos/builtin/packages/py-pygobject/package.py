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


class PyPygobject(AutotoolsPackage):
    """bindings for the GLib, and GObject,
       to be used in Python."""

    homepage = "https://pypi.python.org/pypi/pygobject"
    url      = "https://pypi.python.org/packages/6d/15/97c8b5ccca2be14cf59a2f79e15e3a82a1c3408a6b76b4107689a8b94846/pygobject-2.28.3.tar.bz2"

    version('2.28.3', 'aa64900b274c4661a5c32e52922977f9')

    extends('python')
    depends_on("libffi")
    depends_on('glib')
    depends_on('py-py2cairo')
    depends_on('gobject-introspection')

    patch('pygobject-2.28.6-introspection-1.patch')

    def install(self, spec, prefix):
        make('install', parallel=False)
