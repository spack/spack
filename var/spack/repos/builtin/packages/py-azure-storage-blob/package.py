# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyAzureStorageBlob(PythonPackage):
    """Microsoft Azure Blob Storage Client Library for Python"""

    homepage = "https://github.com/Azure/azure-storage-python"
    pypi = "azure-storage-blob/azure-storage-blob-12.9.0.zip"
    maintainers = ['marcusboden']

    version('12.9.0', sha256='cff66a115c73c90e496c8c8b3026898a3ce64100840276e9245434e28a864225')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-core@1.10:1', type=('build', 'run'))
    depends_on('py-msrest@0.6.21:', type=('build', 'run'))
    depends_on('py-cryptography@2.1.4:', type=('build', 'run'))

    depends_on('py-futures', type=('build', 'run'), when='^python@:2')
    depends_on('py-azure-storage-nspkg@3', type=('build', 'run'), when='^python@:2')

    depends_on('py-enum34@1.0.4:', type=('build', 'run'), when=('^python@:3.3'))
    depends_on('py-typing', type=('build', 'run'), when=('^python@:3.4'))
