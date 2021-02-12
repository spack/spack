# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtWeb(PythonPackage):
    """Microsoft Azure Web Apps Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-web/azure-mgmt-web-0.47.0.zip"

    version('1.0.0',  sha256='c4b218a5d1353cd7c55b39c9b2bd1b13bfbe3b8a71bc735122b171eab81670d1')
    version('0.48.0', sha256='da0f9e3b57528c72a7bc92e3515413a4a4fdbc9626c26ac04b7551a7739a81ec')
    version('0.47.0', sha256='789a328e2a60df48a82452ca6fbc1a7b4adf3c38d4701d278efe4e81cf21cce8')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
