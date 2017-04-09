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
from glob import glob
import os


class Cudnn(Package):
    """NVIDIA cuDNN is a GPU-accelerated library of primitives for deep
    neural networks.

    Note: NVIDIA does not provide a download URL for CUDA so you will
    need to download it yourself. Go to
    https://developer.nvidia.com/rdp/cudnn-download and select your
    Operating System, Architecture, Distribution, and Version.
    Spack will search your current directory for this file.
    Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html.
    """

    homepage = "https://developer.nvidia.com/cudnn"

    version('5.1', '406f4ac7f7ee8aa9e41304c143461a69',
            url="file://%s/cudnn-8.0-linux-x64-v5.1.tgz" % os.getcwd())

    depends_on('cuda@8.0:')

    def install(self, spec, prefix):
        data = glob(os.path.join(self.stage.path, 'cudnn*.tgz'))
        assert len(data) == 1
        tar = which('tar')
        mkdir = which('mkdir')
        mkdir('-p', prefix)
        tar(
            '--directory=%s' % prefix,
            '-x',
            '-z',
            '--strip-components=1',
            '-f%s' % data[0])
