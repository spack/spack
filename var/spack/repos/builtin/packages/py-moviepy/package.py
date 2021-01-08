# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoviepy(PythonPackage):
    """MoviePy is a Python module for video editing, which can
    be used for basic operations (like cuts, concatenations,
    title insertions), video compositing (a.k.a. non-linear
    editing), video processing, or to create advanced effects.
    It can read and write the most common video formats,
    including GIF."""

    homepage = "https://zulko.github.io/moviepy/"
    url      = "https://github.com/Zulko/moviepy/archive/v1.0.3.tar.gz"

    version('1.0.3',      sha256='2bc5f749b614d7d4475096ca8cb59681ad2cf332eeb6fd129e6f8a6e6da5836e')

    depends_on('py-decorator@4.0.2:4.9999', type=('build', 'run'))
    depends_on('py-imageio@2.5:2.9999', when='^python@3.4:', type=('build', 'run'))
    depends_on('py-imageio@2.0:2.4.9999', when='^python@:3.3.9999', type=('build', 'run'))
    depends_on('py-imageio-ffmpeg@0.2.0:', when='^python@3.4:', type=('build', 'run'))
    depends_on('py-tqdm@4.11.2:4.9999', type=('build', 'run'))
    depends_on('py-numpy@1.17.3:', type=('build', 'run'))
    depends_on('py-requests@2.8.1:2.99999', type=('build', 'run'))
    depends_on('py-proglog@:1', type=('build', 'run'))
