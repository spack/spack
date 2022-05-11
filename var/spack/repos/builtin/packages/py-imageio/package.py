# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyImageio(PythonPackage):
    """ Python library for reading and writing image data.

    Imageio is a Python library that provides an easy interface
    to read and write a wide range of image data, including animated
    images, video, volumetric data, and scientific formats. It is
    cross-platform, runs on Python 2.7 and 3.4+, and is easy to install."""

    homepage = "https://github.com/imageio/imageio"
    pypi = "imageio/imageio-2.3.0.tar.gz"

    version('2.16.0', sha256='7f7d8d8e1eb6f8bb1d15e0dd93bee3f72026a4c3b96e9c690e42f403f7bdea3e')
    version('2.10.3', sha256='469c59fe71c81cdc41c84f842d62dd2739a08fac8cb85f5a518a92a6227e2ed6')
    version('2.9.0', sha256='52ddbaeca2dccf53ba2d6dec5676ca7bc3b2403ef8b37f7da78b7654bb3e10f0')
    version('2.5.0', sha256='42e65aadfc3d57a1043615c92bdf6319b67589e49a0aae2b985b82144aceacad')
    version('2.4.1', sha256='16b8077bc8a5fa7a58b3e744f7ecbb156d8c088132df31e0f4f546c98de3514a')
    version('2.3.0', sha256='c4fd5183c342d47fdc2e98552d14e3f24386021bbc3efedd1e3b579d7d249c07')

    # TODO: Add variants for plugins, and optional dependencies

    # Fix for python 2 if needed.
    depends_on('python@3.5:', when='@2.9.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@:2.5.0', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.20:', when='@2.16:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('pil@8.3.2:', when='@2.10:', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('ffmpeg', type='run')
