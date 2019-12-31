# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumcodecs(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/zarr-developers/numcodecs"
    url      = "https://pypi.io/packages/source/n/numcodecs/numcodecs-0.6.4.tar.gz"

    version('0.6.4', sha256='ef4843d5db4d074e607e9b85156835c10d006afc10e175bda62ff5412fca6e4d')

    depends_on('python@2.7:2.8,3.5:',       type=('build', 'run'))
    depends_on('py-setuptools@18.0:',       type='build')
    depends_on('py-setuptools-scm@1.5.4:',  type=('build', 'run'))
    depends_on('py-numpy@1.7:',             type=('build', 'run'))
    depends_on('py-msgpack',                type=('build', 'run'))
