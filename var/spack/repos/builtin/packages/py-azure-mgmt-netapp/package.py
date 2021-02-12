# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMgmtNetapp(PythonPackage):
    """Microsoft Azure NetApp Files Management Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-netapp/azure-mgmt-netapp-0.11.0.zip"

    version('1.0.0',  sha256='e2c0cecd634c0a106e389f39ad767bfd1d718d90692e4e3c9664b1fe9a792ade')
    version('0.15.0', sha256='5e98c360609a77b443b2fe431e0337e5cb705b4f02d0204791f9985f7ce68836')
    version('0.14.0', sha256='6fd915e68d314bec8b56c6ece194005d2c4fc97478fc1f797639d4a6913c1539')
    version('0.13.0', sha256='e86034d073144bd5dbafe17e20fef3f48b5bf98a31b27cc0de462dc8f98303bb')
    version('0.12.0', sha256='7d773119bc02e3d6f9d7cffb7effc17e85676d5c5b1f656d05abc4489e472c76')
    version('0.11.0', sha256='621a76b06c97e858d49b68953e66eb718ac24f91aa6bf090f32a335a38f02305')
    version('0.8.0',  sha256='67df7c7391c2179423a95927a639492c3a177bff8f3a80e4b2d666a86e2d6f6d')

    depends_on('py-setuptools', type='build')
    depends_on('py-msrest@0.5.0:', type=('build', 'run'))
    depends_on('py-msrestazure@0.4.32:1.999', type=('build', 'run'))
    depends_on('py-azure-common@1.1:1.999', type=('build', 'run'))
    depends_on('py-azure-mgmt-nspkg', when='^python@:2', type=('build', 'run'))
