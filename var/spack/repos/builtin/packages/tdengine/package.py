# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tdengine(CMakePackage):
    """An open-source big data platform designed and optimized for the
    Internet of Things (IoT)."""

    homepage = "https://github.com/taosdata/TDengine"
    url      = "https://github.com/taosdata/TDengine/archive/ver-2.0.2.2.tar.gz"

    version('2.0.16.0', sha256='1d741bad0524a799bcfa33f02febf191488836527b8a8431d250bb68d32db2ba')
    version('2.0.15.0', sha256='ab04181dc54e9df9e9fbcc3c655ad38ff24c94e3a6f9f5513254fe8d36ff78d4')
    version('2.0.14.0', sha256='6c481b3c294b9ab96d357fe92f5e99d209c71b4c294a64516fec23fc04004d22')
    version('2.0.13.0', sha256='e178e17e2b8ee2b9dc547cd070887f6c481ffe848fb243d7238d145eb81c0eb4')
    version('2.0.12.0', sha256='874547766bea0fee160bd49197e7d6c925829e823a808326350d714ef4d7ecf7')
    version('2.0.11.0', sha256='0e907acdc2b97d8004b2c60e4cd166d21d06e51c23c731632c3121ae339a4f17')
    version('2.0.10.0', sha256='00c39edf480f20eb2c1fe84adc34d800519a2b668e18c811953f973b039f1c00')
    version('2.0.9.0',  sha256='98bef0e85a9683f6dce2a56595a1d4ea6ee016a96e624d4ad60319ea5f8e4601')
    version('2.0.8.2',  sha256='d6cb2e043a89f3ec9e60d4178709821a8ec3627708b015be794ef99ffaa6edaf')
    version('2.0.8.0',  sha256='a52f4644db2fbe69d20e6cc000bf8c759ce5576e21679da665af9466886c69cb')
    version('2.0.3.2', sha256='3eb8df894998d5592cce377b4f7e267972aee8adf9fc1ce60d1af532ffa9c1c6')
    version('2.0.3.1', sha256='69418815afcac8051f1aab600415669003b4aeec4ec2aaf09cab24636edaf51f')

    @when('target=aarch64:')
    def cmake_args(self):
        args = ['-DCPUTYPE=aarch64']
        return args

    def install(self, spec, prefix):
        install_tree(self.build_directory + '/build', prefix)
