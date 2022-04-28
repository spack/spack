# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRnc2rng(PythonPackage):
    """RELAX NG Compact to regular syntax conversion library."""

    homepage = "https://github.com/djc/rnc2rng"
    pypi     = "rnc2rng/rnc2rng-2.6.5.tar.gz"

    version('2.6.5', sha256='d354afcf0bf8e3b1e8f8d37d71a8fe5b1c0cf75cbd4b71364a9d90b5108a16e5')

    depends_on('py-setuptools', type='build')
    depends_on('py-rply', type=('build', 'run'))
