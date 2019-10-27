# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySemver(PythonPackage):
    """A Python module for semantic versioning.
    Simplifies comparing versions."""

    homepage = "https://semver.org/"
    git      = "https://github.com/k-bx/python-semver.git"

    version('2.8.1', tag='2.8.1')
    version('2.8.0', tag='2.8.0')
    version('2.7.0', tag='2.7.0')
    version('2.6.0', tag='2.6.0')
    version('2.5.0', tag='2.5.0')
    version('2.4.1', tag='2.4.1')

    depends_on('py-setuptools', type='build')
