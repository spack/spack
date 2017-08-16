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


# This isn't really an Autotools package, but it's close enough
# that this works if we override configure().
class Aspell6En(AutotoolsPackage):
    """English (en) dictionary for aspell."""

    extends('aspell')

    homepage = "http://aspell.net/"
    url      = "ftp://ftp.gnu.org/gnu/aspell/dict/en/aspell6-en-2017.01.22-0.tar.bz2"

    version('2017.01.22-0', 'a6e002076574de9dc4915967032a1dab')

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
