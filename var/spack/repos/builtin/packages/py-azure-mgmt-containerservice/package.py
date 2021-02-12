# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtContainerservice(PythonPackage):
    """Microsoft Azure Container Service Management Client Library for Python.
    """

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-containerservice/azure-mgmt-containerservice-9.2.0.zip"

    version('14.0.0', sha256='fbb13448fb52a4090ee91940ae8676403dbe8ae81044b7a5cd3c9e58b47d66de')
    version('11.0.0', sha256='492ec7eb7207fe9aaa53922dc0fc3fd9e7f3b1e42094124f105180011260aa17')
    version('10.1.0', sha256='98f5171b519eb18cb54cc1bdf2bb23d4c377e04e062447721a550f5904319ef0')
    version('10.0.0', sha256='9b44b2d0b281fc1999324a715fb5cf4f47d392a35bc0a01f24bb8dbc4c123acd')
    version('9.4.0',  sha256='d90684106c70779450b82067be4d3e449c799ca1f47d941e45f6d2b5c016dac9')
    version('9.3.0',  sha256='04ca071d1d6af854b6a5947c5aed803924ccbd2ea0d240285b6fa68dc4ab75a9')
    version('9.2.0', sha256='e7904b60c42a153b64b1604f3c698602686b38787bebdaed6e808cd43b6e5967')
    version('9.0.1', sha256='7e4459679bdba4aa67a4b5848e63d94e965a304a7418ef7607eb7a9ce295d886')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
