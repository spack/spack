# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtPolicyinsights(PythonPackage):
    """Microsoft Azure Policy Insights Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-policyinsights/azure-mgmt-policyinsights-0.5.0.zip"

    version('1.0.0', sha256='75103fb4541aeae30bb687dee1fedd9ca65530e6b97b2d9ea87f74816905202a')
    version('0.6.0', sha256='2c64533f6eab08dc16450fc5d7c7651557fc0edc8ef1278dda336333d648a7c4')
    version('0.5.0', sha256='ed229e3845c477e88dde413825d4fba0d38b3a5ffab4e694c7d0da995f3db0f3')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
