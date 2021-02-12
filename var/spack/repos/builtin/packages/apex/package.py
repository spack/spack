# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apex(CMakePackage):
    """Autonomic Performance Environment for eXascale (APEX)."""

    homepage = "http://github.com/khuck/xpress-apex"
    url      = "http://github.com/khuck/xpress-apex/archive/v0.1.tar.gz"

    version('2.3.1', sha256='86bf6933f2c53531fcb24cda9fc7dc9919909bed54740d1e0bc3e7ce6ed78091')
    version('2.3.0', sha256='7e1d16c9651b913c5e28abdbad75f25c55ba25e9fa35f5d979c1d3f9b9852c58')
    version('2.2.0', sha256='cd5eddb1f6d26b7dbb4a8afeca2aa28036c7d0987e0af0400f4f96733889c75c')
    version('2.1.9', sha256='1e134f3a7e6e0e916fa390669abee4c8b45b9e64b47f3a536ffb9d142a6865be')
    version('2.1.8', sha256='a57276efb7811b491e5210f40167efc391d101279f941c22645a4e6243b7b3bc')
    version('2.1.7', sha256='ae75ce8cbb6b6e6afdb99aa09f53c83b5b1577568fe8b2a39cce5d05f744a2e8')
    version('2.1.6', sha256='1f6edae35a5293f507d6fd2b254505255e2165bb2f97713adb0317bcc0c0330a')
    version('2.1.5', sha256='947a8bcfdfc17cd82815301d624c807a0cad05dee5994b8361886581718f39e4')
    version('2.1.4', sha256='a0c28b3d15c3e2dd2511c81ff5afa2a13ebce337b0dfc0b4a9d6800e03e41ba6')
    version('2.1.3', sha256='597d93d55db92bccffbd1f7d9b8cb21f0ada7ae07363195ec78c1f6e06991ac7')
    version('0.1',   sha256='efd10f38a61ebdb9f8adee9dc84acaee22d065b2e6eea1888872a7bfca0f4495')

    depends_on("binutils+libiberty@:2.33.1")
    depends_on("boost@1.54:")
    depends_on('cmake@2.8.12:', type='build')
    depends_on("activeharmony@4.5:")
    depends_on("ompt-openmp")

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBOOST_ROOT=%s' % spec['boost'].prefix,
            '-DUSE_BFD=TRUE',
            '-DBFD_ROOT=%s' % spec['binutils'].prefix,
            '-DUSE_ACTIVEHARMONY=TRUE',
            '-DACTIVEHARMONY_ROOT=%s' % spec['activeharmony'].prefix,
            '-DUSE_OMPT=TRUE',
            '-DOMPT_ROOT=%s' % spec['ompt-openmp'].prefix,
        ]
