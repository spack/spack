##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os


class OctaveStruct(Package):
    """Additional structure manipulation functions for Octave."""

    homepage = "https://octave.sourceforge.io/struct/"
    url      = "https://downloads.sourceforge.net/octave/struct-1.0.14.tar.gz"

    version('1.0.14', '3589d5eb8000f18426e2178587eb82f4')

    extends('octave@2.9.7:')

    def install(self, spec, prefix):
        os.environ.pop('CC', '')
        os.environ.pop('CXX', '')
        os.environ.pop('FC', '')
        octave('--quiet',
               '--norc',
               '--built-in-docstrings-file=/dev/null',
               '--texi-macros-file=/dev/null',
               '--eval', 'pkg prefix %s; pkg install %s' %
               (prefix, self.stage.archive_file))
