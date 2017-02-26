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
import os.path
from glob import glob


class Highwayhash(MakefilePackage):
    """Strong (well-distributed and unpredictable) hashes:
	- Portable implementation of SipHash
	- HighwayHash, a 5x faster SIMD hash with security claims
    """
 
    homepage = "https://github.com/google/highwayhash"
 
    version('dfcb97', git='https://github.com/google/highwayhash.git',
	    commit='dfcb97ca4fe9277bf9dc1802dd979b071896453b')  

    build_targets = ['all', 'libhighwayhash.a']
 
    def install(self, spec, prefix):
	install('libhighwayhash.a', prefix.lib)
	for i in glob('highwayhash/*.h'):
	    install(i, prefix.bin)
