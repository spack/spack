# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtSearch(PythonPackage):
    """Microsoft Azure Search Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-search/azure-mgmt-search-2.1.0.zip"

    version('8.0.0', sha256='a96d50c88507233a293e757202deead980c67808f432b8e897c4df1ca088da7e')
    version('3.0.0', sha256='d4c78b14b48edd2e27e2068c9a448acfc84a18595be77fe483afe7bb447e1eb6')
    version('2.1.0', sha256='92a40a1a7a9e3a82b6fa302042799e8d5a67d3996c20835af72afc14f1610501')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
