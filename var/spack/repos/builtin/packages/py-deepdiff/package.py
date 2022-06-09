# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeepdiff(PythonPackage):
    """Deep Difference and Search of any Python object/data.."""

    homepage = "https://github.com/seperman/deepdiff"
    pypi = "deepdiff/deepdiff-5.6.0.tar.gz"

    version('5.6.0', sha256='e3f1c3a375c7ea5ca69dba6f7920f9368658318ff1d8a496293c79481f48e649')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-ordered-set@4.0.2', type=('build', 'run'))
