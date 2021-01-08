# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImageioFfmpeg(PythonPackage):
    """The purpose of this project is to provide a simple and
    reliable ffmpeg wrapper for working with video files. It
    implements two simple generator functions for reading and
    writing data from/to ffmpeg, which reliably terminate the
    ffmpeg process when done. It also takes care of publishing
    platform-specific wheels that include the binary ffmpeg
    executables."""

    homepage = "https://github.com/imageio/imageio-ffmpeg"
    url      = "https://github.com/imageio/imageio-ffmpeg/archive/v0.4.3.tar.gz"

    version('0.4.3', sha256='906680ae784d79972671c6a0adf5ce1604703506def9096d346f758a6a52bf6f')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('ffmpeg', type='run')
