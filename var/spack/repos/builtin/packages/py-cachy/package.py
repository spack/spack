# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCachy(PythonPackage):
    """Cachy provides a simple yet effective caching library."""

    homepage = "https://github.com/sdispater/cachy"
    pypi     = "cachy/cachy-0.3.0.tar.gz"

    version('0.3.0', sha256='186581f4ceb42a0bbe040c407da73c14092379b1e4c0e327fdb72ae4a9b269b1')

    depends_on('python@2.7,3.4:4', type=('build', 'run'))
    # https://github.com/sdispater/cachy/issues/20
    depends_on('py-setuptools', type='build')
