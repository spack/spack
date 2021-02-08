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
    pypi     = "msgpack-numpy/msgpack-numpy-0.4.7.1.tar.gz"

    version('0.4.7.1', sha256='7eaf51acf82d7c467d21aa71df94e1c051b2055e54b755442051b474fa7cf5e1')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9:', type=('build', 'run'))
    depends_on('py-msgpack@0.5.2:', type=('build', 'run'))
