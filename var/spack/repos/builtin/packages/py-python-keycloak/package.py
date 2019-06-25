# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonKeycloak(PythonPackage):
    """Python package providing access to the Keycloak API."""

    homepage = "https://python-keycloak.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-keycloak/python-keycloak-0.17.2.tar.gz"

    version('0.17.2', 'a7dd430dea215d420cb0e3b97e638c3d')

    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type='run')
    depends_on('py-python-jose', type='run')
