# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtServicebus(PythonPackage):
    """Microsoft Azure Service Bus Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-servicebus/azure-mgmt-servicebus-0.6.0.zip"

    version('6.0.0', sha256='f6c64ed97d22d0c03c4ca5fc7594bd0f3d4147659c10110160009b93f541298e')
    version('2.0.0', sha256='e06bff420bb6b87a0fd5e21a946964d730e89b9dff6fce8da28b89e62e846611')
    version('1.0.0', sha256='bb37d97eb3798740a0bc1bfa37b04946a193a6d1a3b0849fdc5e1dc2a9f25d81')
    version('0.6.0', sha256='f20920b8fb119ef4abeda4d2dac765a4fc48cd0bcf30c27f8c4cc6d890bc08b1')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
