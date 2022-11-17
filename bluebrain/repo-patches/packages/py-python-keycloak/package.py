# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonKeycloak(PythonPackage):
    """Python package providing access to the Keycloak API."""

    homepage = "https://python-keycloak.readthedocs.io/en/latest"
    pypi = "python-keycloak/python-keycloak-2.6.0.tar.gz"

    version('2.6.0', sha256='08c530ff86f631faccb8033d9d9345cc3148cb2cf132ff7564f025292e4dbd96')

    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type='run')
    depends_on('py-python-jose', type='run')
    depends_on('py-urllib3', type='run')
    depends_on('py-requests-toolbelt', type='run')
