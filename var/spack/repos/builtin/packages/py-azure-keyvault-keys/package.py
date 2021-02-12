# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureKeyvaultKeys(PythonPackage):
    """Microsoft Azure Key Vault Keys Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-keys"
    pypi = "azure-keyvault-keys/azure-keyvault-keys-4.1.0.zip"

    version('4.3.1', sha256='fbf67bca913ebf68b9075ee9d2e2b899dc3c7892cc40abfe1b08220a382f6ed9')
    version('4.3.0', sha256='064a98791fe447a0e57850bb5ec1ec43e7d5fd39266319b5acc44a9704a3b966')
    version('4.2.0', sha256='e47b76ca5d99b12436c64ce4431271cd6744fba017f282991b84ce303e0b9eaa')
    version('4.1.0', sha256='f9967b4deb48e619f6c40558f69e48978779cc09c8a7fad33d536cfc41cd68f9')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-core@1.2.1:1.999', type=('build', 'run'))
    depends_on('py-cryptography@2.1.4:', type=('build', 'run'))
    depends_on('py-msrest@0.6.0:', type=('build', 'run'))
    depends_on('py-azure-keyvault-nspkg', when='^python@:2', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-typing', when='^python@:3.4', type=('build', 'run'))
