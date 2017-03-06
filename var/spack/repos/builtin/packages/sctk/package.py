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
from distutils.dir_util import copy_tree


class Sctk(Package):
    """The NIST Scoring Toolkit (SCTK) is a collection of software tools 
        designed to score benchmark test evaluations of Automatic Speech 
        Recognition (ASR) Systems. The toolkit is currently used by NIST, 
        benchmark test participants, and reserchers worldwide to as a 
        common scoring engine."""

    homepage = "https://www.nist.gov/itl/iad/mig/tools"
    url      = "http://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2"

    version('2.4.10', 'dd01ad49a33486a4754655d06177f646',
            url='http://www.openslr.org/resources/4/sctk-2.4.10-20151007-1312Z.tar.bz2')
    version('2.4.9', '8cdab2a1263fe103481e23776e2178a1',
            url='http://www.openslr.org/resources/4/sctk-2.4.9-20141015-1634Z.tar.bz2')
    version('2.4.8', '2385209185b584e28dc42ea2cd324478',
            url='http://www.openslr.org/resources/4/sctk-2.4.8-20130429-2145.tar.bz2')
    version('2.4.0', '77912e75304098ffcc6850ecf641d1a4',
            url='http://www.openslr.org/resources/4/sctk-2.4.0-20091110-0958.tar.bz2')

    def install(self, spec, prefix):
        make('config')
        make('all')
        make('install')
        mkdirp(prefix.bin)
        copy_tree('bin', prefix.bin)
