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
# Why doesn't this work for me?
# from spack import *
from llnl.util.filesystem import filter_file
from spack.build_systems.autotools import AutotoolsPackage
from spack.directives import extends
from spack.package import ExtensionError
from spack.util.executable import which


#
# Aspell dictionaries install their bits into their prefix.lib
# and when activated they'll get symlinked into the appropriate aspell's
# dict dir (see aspell's {de,}activate methods).
#
# They aren't really an Autotools package, but it's close enough
# that this works if we override configure().
class AspellDictPackage(AutotoolsPackage):
    """Specialized class for building aspell dictionairies."""

    extends('aspell')

    def view_destination(self, view):
        aspell_spec = self.spec['aspell']
        if view.root != aspell_spec.prefix:
            raise ExtensionError(
                'aspell does not support non-global extensions')
        aspell = aspell_spec.command
        return aspell('dump', 'config', 'dict-dir', output=str).strip()

    def view_source(self):
        return self.prefix.lib

    def patch(self):
        filter_file(r'^dictdir=.*$', 'dictdir=/lib', 'configure')
        filter_file(r'^datadir=.*$', 'datadir=/lib', 'configure')

    def configure(self, spec, prefix):
        aspell = spec['aspell'].prefix.bin.aspell
        prezip = spec['aspell'].prefix.bin.prezip
        destdir = prefix

        sh = which('sh')
        sh('./configure', '--vars', "ASPELL={0}".format(aspell),
           "PREZIP={0}".format(prezip),
           "DESTDIR={0}".format(destdir))
