# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBxPython(PythonPackage):
    """The bx-python project is a python library and associated set of scripts
    to allow for rapid implementation of genome scale analyses."""

    homepage = "https://github.com/bxlab/bx-python"
    url      = "https://github.com/bxlab/bx-python/archive/v0.7.4.tar.gz"

    version('0.7.4', sha256='1066d1e56d062d0661f23c19942eb757bd7ab7cb8bc7d89a72fdc3931c995cb4')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
