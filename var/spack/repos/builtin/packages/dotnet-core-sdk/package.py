# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink
from spack import *


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"
    url      = "https://github.com/dotnet/core/"

    version('2.1.300',
            url='https://download.microsoft.com/download/8/8/5/88544F33-836A'
                '-49A5-8B67-451C24709A8F/dotnet-sdk-2.1.300-linux-x64.tar.gz',
            sha224='80a6bfb1db5862804e90f819c1adeebe3d624eae0d6147e5d6694333'
                'f0458afd7d34ce73623964752971495a310ff7fcc266030ce5aef82d5de'
                '7293d94d13770')

    variant('telemetry', default=False,
            description='allow collection of telemetry data')

    def setup_environment(self, spack_env, run_env):
        if '-telemetry' in self.spec:
            spack_env.set('DOTNET_CLI_TELEMETRY_OPTOUT', 1)

    def install(self, spec, prefix):
        mkdirp('bin')
        symlink('../dotnet', 'bin/dotnet')
        install_tree(".", prefix)
