# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spdlog(CMakePackage):
    """Very fast, header only, C++ logging library"""

    homepage = "https://github.com/gabime/spdlog"
    url = "https://github.com/gabime/spdlog/archive/v0.9.0.tar.gz"

    version('1.4.1', sha256='3291958eb54ed942d1bd3aef1b4f8ccf70566cbc04d34296ec61eb96ceb73cff')
    version('1.2.1', sha256='867a4b7cedf9805e6f76d3ca41889679054f7e5a3b67722fe6d0eae41852a767')
    version('1.2.0', sha256='0ba31b9e7f8e43a7be328ab0236d57810e5d4fc8a1a7842df665ae22d5cbd128')
    version('1.1.0',  sha256='3dbcbfd8c07e25f5e0d662b194d3a7772ef214358c49ada23c044c4747ce8b19')
    version('1.0.0',  sha256='90d5365121bcd2c41ce94dfe6a460e89507a2dfef6133fe5fad5bb35ac4ef0a1')
    version('0.17.0', sha256='94f74fd1b3344733d1db3de2ec22e6cbeb769f93a8baa0d4a22b1f62dc7369f8')
    version('0.16.3', sha256='b88d7be261d9089c817fc8cee6c000d69f349b357828e4c7f66985bc5d5360b8')
    version('0.16.2', sha256='2081e5df5e87402398847431e16b87c71dd5c4d632314bb976ace8161f4d32de')
    version('0.16.1', sha256='733260e1fbdcf1b3dc307fc585e4476240026de8be28eb905731d2ab0942deae')
    version('0.16.0', sha256='9e64e3b10c2a3c54dfff63aa056057cf1db8a5fd506b3d9cf77207511820baac')
    version('0.14.0', sha256='eb5beb4e53f4bfff5b32eb4db8588484bdc15a17b90eeefef3a9fc74fec1d83d')
    version('0.13.0', sha256='d798a6ca19165f0a18a43938859359269f5a07fd8e0eb83ab8674739c9e8f361')
    version('0.12.0', sha256='5cfd6a0b3182a88e1eb35bcb65a7ef9035140d7c73b16ba6095939dbf07325b9')
    version('0.11.0', '08232203f18a6f9ff47e083cc7a141a050805d3b')
    version('0.10.0', '57b471ef97a23cc29c38b62e00e89a411a87ea7f')
    version('0.9.0', 'dda741ef8e12d57d91f778d85e95a27d84a82ac4')

    variant('shared', default=True,
            description='Build shared libraries (v1.4.0+)')

    depends_on('cmake@3.2:', type='build')

    def cmake_args(self):
        spec = self.spec

        args = []

        if self.spec.version >= Version('1.4.0'):
            args.extend([
                '-DSPDLOG_BUILD_SHARED:BOOL={0}'.format(
                    'ON' if '+shared' in spec else 'OFF'),
                # tests and examples
                '-DSPDLOG_BUILD_TESTS:BOOL={0}'.format(
                    'ON' if self.run_tests else 'OFF'),
                '-DSPDLOG_BUILD_EXAMPLE:BOOL={0}'.format(
                    'ON' if self.run_tests else 'OFF')
            ])

        return args
