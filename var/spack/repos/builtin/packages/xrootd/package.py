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


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
       tolerant access to data repositories of many kinds."""
    homepage = "http://xrootd.org"
    url      = "http://xrootd.org/download/v4.6.0/xrootd-4.6.0.tar.gz"

    version('4.8.3', 'bb6302703ffc123f7f9141ddb589435e')
    version('4.8.2', '531b632191b59c2cf76ab8d31af4a866')
    version('4.8.1', 'a307973f7f43b0cc2688dfe502e17709')
    version('4.8.0', '4349e7f664e686b72855e894b49063ad')
    version('4.7.1', '4006422bcf99e0a19996ace4ebb99175')
    version('4.7.0', '2a92ba483f574c6ba6a9ff061878af22')
    version('4.6.1', '70c6f6e1f5f2b4eeb3c7d2c41a36bb2c')
    version('4.6.0', '5d60aade2d995b68fe0c46896bc4a5d1')
    version('4.5.0', 'd485df3d4a991e1c35efa4bf9ef663d7')
    version('4.4.1', '72b0842f802ccc94dede4ac5ab2a589e')
    version('4.4.0', '58f55e56801d3661d753ff5fd33dbcc9')
    version('4.3.0', '39c2fab9f632f35e12ff607ccaf9e16c')

    variant('http', default=True,
            description='Build with HTTP support')

    variant('python', default=False,
            description='Build pyxroot Python extension')

    variant('readline', default=True,
            description='Use readline')

    depends_on('bzip2')
    depends_on('cmake@2.6:', type='build')
    depends_on('libxml2', when='+http')
    depends_on('openssl')
    depends_on('python', when='+python')
    depends_on('readline', when='+readline')
    depends_on('xz')
    depends_on('zlib')

    extends('python', when='+python')
    patch('python-support.patch', level=1, when='+python')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DENABLE_HTTP:BOOL={0}'.
            format('ON' if '+http' in spec else 'OFF'),
            '-DENABLE_PYTHON:BOOL={0}'.
            format('ON' if '+python' in spec else 'OFF'),
            '-DENABLE_READLINE:BOOL={0}'.
            format('ON' if '+readline' in spec else 'OFF'),
            '-DENABLE_CEPH:BOOL=OFF'
        ]
        return options
