# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtHdinsight(PythonPackage):
    """Microsoft Azure HDInsight Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-hdinsight/azure-mgmt-hdinsight-1.5.1.zip"

    version('7.0.0', sha256='d0070817ee2be611d45af91eabc5665dd53f024eaa7a55e490ace4f71a55c733')
    version('2.2.0', sha256='332c60dc6d3e38093f6e1e24e5338418626ec8406d600d9e74d95b2179d61383')
    version('2.1.0', sha256='ed55df52d35fc03a9c7ca060af1ec0faf7b5510381d2a5e74b73f59ac0d79028')
    version('2.0.0', sha256='fd47029f2423e45ec4d311f651dc972043b98e960f186f5c6508c6fdf6eb2fe8')
    version('1.7.0', sha256='9d1120bd9760687d87594ec5ce9257b7335504afbe55b3cda79462c1e07a095b')
    version('1.6.0', sha256='b1d06279307c41da5e0a5c9722aa6b36ce3b2c212534a54767210639451b9800')
    version('1.5.1', sha256='76b94f3e43fdc6698023d79be731937dc645dc3178dc134854768528ecc0aea3')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
