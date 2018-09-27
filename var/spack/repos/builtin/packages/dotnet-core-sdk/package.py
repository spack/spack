##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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
