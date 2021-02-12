# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtNetwork(PythonPackage):
    """Microsoft Azure Network Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-network/azure-mgmt-network-11.0.0.zip"

    version('17.1.0', sha256='f47852836a5960447ab534784a9285696969f007744ba030828da2eab92621ab')
    version('17.0.0', sha256='3694f2675e152afccb1588a6cc7bb4b4795d442a4e5d7082cdf1f4e32a779199')
    version('16.0.0', sha256='6159a8c44590cc58841690c27c7d4acb0cd9ad0a1e5178c1d35e0f48e3c3c0e9')
    version('13.0.0', sha256='084b4253ef61e26a72cad3eb00e7adbfd0e54cf738498392e70d73a21d294c09')
    version('12.0.0', sha256='74502996a4d6c7b3b72e3f57c2ff297263cc02f18fec33363582346a29390094')
    version('11.0.0', sha256='7fdfc631c660cb173eee88abbb7b8be7742f91b522be6017867f217409cd69bc')
    version('10.2.0', sha256='d50c74cdc1c9be6861ddef9adffd3b05afc5a5092baf0209eea30f4439cba2d9')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
