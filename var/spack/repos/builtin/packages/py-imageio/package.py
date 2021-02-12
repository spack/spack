# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
    pypi = "imageio/imageio-2.3.0.tar.gz"

    version('2.9.0', sha256='52ddbaeca2dccf53ba2d6dec5676ca7bc3b2403ef8b37f7da78b7654bb3e10f0')
    version('2.8.0', sha256='fb5fd6d3d17126bbaac9af29fe340e2c97a196eb9416d4f28c0e543744a152cf')
    version('2.6.1', sha256='f44eb231b9df485874f2ffd22dfd0c3c711e7de076516b9374edea5c65bc67ae')
    version('2.6.0', sha256='cfafaedf42bc8cdc7d45b0886b0e332932729492a6d04d46123a8f32f95c3583')
    version('2.5.0', sha256='42e65aadfc3d57a1043615c92bdf6319b67589e49a0aae2b985b82144aceacad')
    version('2.4.1', sha256='16b8077bc8a5fa7a58b3e744f7ecbb156d8c088132df31e0f4f546c98de3514a')
    version('2.3.0', sha256='c4fd5183c342d47fdc2e98552d14e3f24386021bbc3efedd1e3b579d7d249c07')

    # TODO: Add variants for plugins, and optional dependencies

    # Fix for python 2 if needed.
    depends_on('py-numpy',            type=('build', 'run'))
    depends_on('pil',                 type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('ffmpeg',              type='run')
