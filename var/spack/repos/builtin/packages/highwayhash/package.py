##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
from glob import glob
import os


class Highwayhash(MakefilePackage):
    """Strong (well-distributed and unpredictable) hashes:
        - Portable implementation of SipHash
        - HighwayHash, a 5x faster SIMD hash with security claims
    """

    homepage = "https://github.com/google/highwayhash"

    version('be5491d', git='https://github.com/google/highwayhash.git',
            commit='be5491d449e9cc411a1b4b80a128f5684d50eb4c')

    build_targets = ['all']

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.include)

        # The following are CPU and compiler flag specific
        if(os.path.exists('lib/libhighwayhash.a')):
            mkdirp(prefix.lib)
            install('lib/libhighwayhash.a', prefix.lib)
        if(os.path.exists('highwayhash_test')):
            install('highwayhash_test', prefix.bin)
        if(os.path.exists('benchmark')):
            install('benchmark', prefix.bin)

        # Always installed
        install('bin/profiler_example', prefix.bin)
        install('bin/nanobenchmark_example', prefix.bin)
        install('bin/vector_test', prefix.bin)
        install('bin/sip_hash_test', prefix.bin)
        for i in glob('highwayhash/*.h'):
            install(i, prefix.include)
