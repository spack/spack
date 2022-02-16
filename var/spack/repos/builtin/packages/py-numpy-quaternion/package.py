# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumpyQuaternion(PythonPackage):
    """This package creates a quaternion type in python, and further enables
    numpy to create and manipulate arrays of quaternions. The usual algebraic
    operations (addition and multiplication) are available, along with numerous
    properties like norm and various types of distance measures between two
    quaternions. There are also additional functions like “squad” and “slerp”
    interpolation, and conversions to and from axis-angle, matrix, and
    Euler-angle representations of rotations. The core of the code is written in
    C for speed."""

    homepage = "https://github.com/moble/quaternion"
    pypi     = "numpy-quaternion/numpy-quaternion-2021.11.4.15.26.3.tar.gz"

    version('2021.11.4.15.26.3', sha256='b0dc670b2adc8ff2fb8d6105a48769873f68d6ccbe20af6a19e899b1e8d48aaf')

    depends_on('py-setuptools',         type='build')
    depends_on('py-numpy@1.13:',        type=('build', 'run'))
