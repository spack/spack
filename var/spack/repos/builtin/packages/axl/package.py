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
from spack import *
from spack.error import SpackError


def async_api_validator(values):
    if 'none' in values and len(values) != 1:
        raise SpackError("The value 'none' is not usable"
                         " with other async_api values.")
    if 'ibm_bbapi' in values and 'cray_dw' in values:
        raise SpackError("The 'ibm_bbapi' and 'cray_dw' asynchronous"
                         " APIs are incompatible.")


class Axl(CMakePackage):
    """Asynchronous transfer library"""

    homepage = "https://github.com/ECP-VeloC/AXL"
    url      = "https://github.com/ECP-VeloC/AXL/archive/v0.1.0.zip"
    git      = "https://github.com/ecp-veloc/axl.git"

    tags = ['ecp']

    version('master', branch='master')
    version('0.1.1', sha256='7ec0417447c5a3cc0b6e46ff3f646984410c77e6c2081cf0c748781384be739b')

    variant('async_api', default='daemon',
            description="Set of async transfer APIs to enable",
            values=['cray_dw', 'ibm_bbapi', 'daemon', 'none'], multi=True,
            validator=async_api_validator)

    # not-yet implemented functionality
    conflicts('async_api=cray_dw', when='@0.1.0')
    conflicts('async_api=ibm_bbapi', when='@0.1.0')

    depends_on('kvtree')

    def cmake_args(self):
        args = []
        if self.spec.satisfies('platform=cray'):
            args.append("-DAXL_LINK_STATIC=ON")
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec['kvtree'].prefix)

        apis = list(self.spec.variants['async_api'].value)
        if 'daemon' in apis:
            args.append('-DAXL_ASYNC_DAEMON=ON')
            apis.remove('daemon')

        for api in apis:
            args.append('-DAXL_ASYNC_API={0}'.format(api))

        return args
