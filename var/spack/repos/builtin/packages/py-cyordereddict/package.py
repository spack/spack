# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCyordereddict(PythonPackage):
    """The Python standard library's OrderedDict ported to Cython.
    A drop-in replacement that is 2-6x faster."""

    homepage = "https://github.com/shoyer/cyordereddict"
    url      = "https://files.pythonhosted.org/packages/d1/1a/364cbfd927be1b743c7f0a985a7f1f7e8a51469619f9fefe4ee9240ba210/cyordereddict-1.0.0.tar.gz"

    version('1.0.0', sha256='d9b2c31796999770801a9a49403b8cb49510ecb64e5d1e9d4763ed44f2d5a76e')

    depends_on('python@2.7:2.8', type=('build', 'run'))
