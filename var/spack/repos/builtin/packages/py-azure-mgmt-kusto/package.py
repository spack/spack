# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtKusto(PythonPackage):
    """Microsoft Azure Kusto Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-kusto/azure-mgmt-kusto-0.9.0.zip"

    version('1.0.0',  sha256='fa3ede0ebd6489bbf993f420bcb5fc63d9fad2a1e945c3c49b26fa012bb3534e')
    version('0.10.0', sha256='09e8d4928e19d12feb374adb47651b474f3ee3bc6a12704e4b70c9b38e3bcd9e')
    version('0.9.0', sha256='9210db89fa18ee8ed53339cd63bbe6fe1d9624cd793b54b7451ddbda8ae92ef3')
    version('0.3.0', sha256='9eb8b7781fd4410ee9e207cd0c3983baf9e58414b5b4a18849d09856e36bacde')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
