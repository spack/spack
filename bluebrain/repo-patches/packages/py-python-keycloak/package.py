# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonKeycloak(PythonPackage):
    """Python package providing access to the Keycloak API."""

    homepage = "https://python-keycloak.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-keycloak/python-keycloak-0.24.0.tar.gz"

    version('0.24.0', sha256='f21ba80385e128eb24159d132b12254c3171d83080a1e6bf7e7dd5590c0b82b1')

    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type='run')
    depends_on('py-python-jose', type='run')
