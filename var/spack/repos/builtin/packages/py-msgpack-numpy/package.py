# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMsgpackNumpy(PythonPackage):
    """This package provides encoding and decoding routines
    that enable the serialization and deserialization of
    numerical and array data types provided by numpy using the
    highly efficient msgpack format. Serialization of Python's
    native complex data types is also supported."""

    homepage = "https://github.com/lebedov/msgpack-numpy"
    url      = "https://github.com/lebedov/msgpack-numpy/archive/0.4.7.1.tar.gz"

    version('0.4.7.1', sha256='c1f3fc082efbf733aeb24aa638db622b8f6d6320a82b19116dc97e7afd0ab5cc')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-msgpack@0.5.2:', type=('build', 'run'))
