# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWheel(PythonPackage):
    """A built-package format for Python."""

    homepage = "https://pypi.python.org/pypi/wheel"
    url      = "https://pypi.io/packages/source/w/wheel/wheel-0.29.0.tar.gz"

    version('0.33.1', sha256='66a8fd76f28977bb664b098372daef2b27f60dc4d1688cfab7b37a09448f0e9d')
    version('0.29.0', sha256='1ebb8ad7e26b448e9caa4773d2357849bf80ff9e313964bcaf79cbf0201a1648')
    version('0.26.0', sha256='eaad353805c180a47545a256e6508835b65a8e830ba1093ed8162f19a50a530c')

    depends_on('py-setuptools', type='build')
