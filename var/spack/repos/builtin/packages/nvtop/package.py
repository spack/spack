# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nvtop(CMakePackage):
    """Nvtop stands for NVidia TOP, a (h)top like task monitor for NVIDIA GPUs.
    It can handle multiple GPUs and print information about them
    in a htop familiar way."""

    homepage = "https://github.com/Syllo/nvtop"
    url      = "https://github.com/Syllo/nvtop/archive/1.1.0.tar.gz"

    version('1.1.0', sha256='00470cde8fc48d5a5ed7c96402607e474414d94b562b21189bdde1dbe6b1d1f3')

    depends_on('cmake')
    depends_on('ncurses')
    depends_on('git')
    depends_on('cuda')
    depends_on('py-pynvml', type=('build', 'run'))
    depends_on('py-nvidia-ml-py3', type=('build', 'run'))

    def cmake_args(self):
        cmake_args = []
        cmake_args.append('-DNVML_RETRIEVE_HEADER_ONLINE=True')
        return cmake_args
