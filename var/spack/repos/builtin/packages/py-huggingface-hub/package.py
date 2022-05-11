# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyHuggingfaceHub(PythonPackage):
    """This library allows anyone to work with the Hub
    repositories: you can clone them, create them and upload
    your models to them."""

    homepage = "https://github.com/huggingface/huggingface_hub"
    pypi     = "huggingface_hub/huggingface_hub-0.0.10.tar.gz"

    version('0.0.10', sha256='556765e4c7edd2d2c4c733809bae1069dca20e10ff043870ec40d53e498efae2')
    version('0.0.8', sha256='be5b9a7ed36437bb10a780d500154d426798ec16803ff3406f7a61107e4ebfc2')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-filelock', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-typing-extensions', when='@0.0.10:', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='^python@:3.7', type=('build', 'run'))
