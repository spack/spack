# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPybind11Stubgen(PythonPackage):
    """Generates stubs for pybind11-wrapped python modules"""

    homepage = "https://github.com/sizmailov/pybind11-stubgen"
    pypi     = "pybind11-stubgen/pybind11-stubgen-0.3.0.tar.gz"

    version('0.3.0', sha256='fb9bc977df46d7f1aecd33258e34abbbd01f1f461862c8a2a85341b96e6e6bdf')

    depends_on('py-setuptools',     type='build')
