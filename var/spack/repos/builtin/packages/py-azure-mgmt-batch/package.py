# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtBatch(PythonPackage):
    """Microsoft Azure Batch Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-batch/azure-mgmt-batch-9.0.0.zip"

    version('15.0.0', sha256='9b793bb31a0d4dc8c29186db61db24d83795851a75846aadb187cf95bf853ccb')
    version('14.0.0', sha256='1d3b2c9ebd57c8874e11d29e7dd05a1f078d2156fc9683e2f2ad41024e448bf6')
    version('10.0.1', sha256='455e2f1010a59163bfd25d72e9d8dc7847df566795bc35655bcb2de925763d33')
    version('10.0.0', sha256='5c446f5bdab0a2e2678b6efb6a1a7f7046754ae928b20e077c17026d248f5036')
    version('9.0.0', sha256='03417eecfa1fac906e674cb1cb43ed7da27a96277277b091d7c389ba39f6c3fe')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
