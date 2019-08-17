# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImageio(PythonPackage):
    """ Imageio is a Python library that provides an easy interface
    to read and write a wide range of image data, including animated
    images, video, volumetric data, and scientific formats. It is
    cross-platform, runs on Python 2.7 and 3.4+, and is easy to install."""

    homepage = "http://imageio.github.io/"
    url      = "https://pypi.io/packages/source/i/imageio/imageio-2.3.0.tar.gz"

    version('2.3.0', '4722c4e1c366748abcb18729881cffb8')

    # TODO: Add variants for plugins, and optional dependencies

    # Fix for python 2 if needed.
    depends_on('py-numpy',            type=('build', 'run'))
    depends_on('py-pillow',           type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('ffmpeg',              type='run')
