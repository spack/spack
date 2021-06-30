# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorflowAddons(PythonPackage):
    """TensorFlow Addons."""

    homepage = "https://pypi.org/project/tensorflow-addons/"
    url = "https://github.com/tensorflow/addons/archive/refs/tags/v0.13.0.tar.gz"

    version('0.13.0', sha256='5a8c33ecef5a3daca7f6b27c4b4e3a2badfe55f55a13e97066ee2e03ef98fab0')

    depends_on('py-setuptools', type='build')
    depends_on('py-tensorflow@2.3:2.5', type=('run'))
    depends_on('py-typeguard@2.7:', type=('run'))
