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
from glob import glob


class Motioncor2(Package):
    """MotionCor2 is a multi-GPU program that corrects beam-induced sample
    motion recorded on dose fractionated movie stacks. It implements a robust
    iterative alignment algorithm that delivers precise measurement and
    correction of both global and non-uniform local motions at
    single pixel level, suitable for both single-particle and
    tomographic images. MotionCor2 is sufficiently fast
    to keep up with automated data collection."""

    homepage = "http://msg.ucsf.edu/em/software"
    url      = "http://msg.ucsf.edu/MotionCor2/MotionCor2-1.0.2.tar.gz"

    version('1.0.4',        '5fc0a35d9518b2df17104187dab63fc6')
    version('1.0.2',        'f2f4c5b09170ab8480ca657f14cdba2b')
    version('1.0.1',        '73d94a80abdef9bf37bbc80fbbe76622')
    version('1.0.0',        '490f4df8daa9f5ddb9eec3962ba3ddf5')

    depends_on('cuda@8.0:8.99', type='run')
    # libtiff.so.3 is required
    depends_on('libtiff@3.0:3.99', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        for files in glob("MotionCor2_*"):
            install(files, prefix.bin)
        with working_dir(prefix.bin):
            symlink('MotionCor2_{0}'.format(spec.version), 'MotionCor2')
