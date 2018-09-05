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


class PyPygobject(PythonPackage):
    """bindings for the GLib, and GObject,
       to be used in Python."""

    homepage = "https://pypi.python.org/pypi/pygobject"

    version('3.28.3', '3bac63c86bb963aa401f97859464aa90')
    version('2.28.6', '9415cb7f2b3a847f2310ccea258b101e')
    version('2.28.3', 'aa64900b274c4661a5c32e52922977f9',
            url='http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.3.tar.bz2')

    extends('python')

    depends_on('py-setuptools', type=('build'))
    depends_on("libffi")
    depends_on('glib')
    depends_on('python@2:2.99', when='@2:2.99', type=('build', 'run'))
    depends_on('py-pycairo', type=('build', 'run'), when='@3:')
    depends_on('py-py2cairo', type=('build', 'run'), when='@2:2.99')
    depends_on('gobject-introspection')
    depends_on('gtkplus', when='@3:')

    patch('pygobject-2.28.6-introspection-1.patch', when='@2.28.3:2.28.6')

    # patch from https://raw.githubusercontent.com/NixOS/nixpkgs/master/pkgs/development/python-modules/pygobject/pygobject-2.28.6-gio-types-2.32.patch
    # for https://bugzilla.gnome.org/show_bug.cgi?id=668522
    patch('pygobject-2.28.6-gio-types-2.32.patch', when='@2.28.6')

    def url_for_version(self, version):
        url = 'http://ftp.gnome.org/pub/GNOME/sources/pygobject'
        return url + '/%s/pygobject-%s.tar.xz' % (version.up_to(2), version)

    # pygobject version 2 requires an autotools build
    @when('@2:2.99')
    def build(self, spec, prefix):
        configure('--prefix=%s' % spec.prefix)

    @when('@2:2.99')
    def install(self, spec, prefix):
        make('install', parallel=False)

    @when('^python@3:')
    def patch(self):
        filter_file(
            r'Pycairo_IMPORT',
            r'//Pycairo_IMPORT',
            'gi/pygi-foreign-cairo.c')
