# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OclIcd(AutotoolsPackage):
    """This package aims at creating an Open Source alternative to vendor specific
OpenCL ICD loaders."""

    homepage = "https://github.com/OCL-dev/ocl-icd"
    url      = "https://github.com/OCL-dev/ocl-icd/archive/v2.2.12.tar.gz"

    version('2.2.12', sha256='17500e5788304eef5b52dbe784cec197bdae64e05eecf38317840d2d05484272')
    version('2.2.11', sha256='c1865ef7701b8201ebc6930ed3ac757c7e5cb30f3aa4c1e742a6bc022f4f2292')
    version('2.2.10', sha256='d0459fa1421e8d86aaf0a4df092185ea63bc4e1a7682d3af261ae5d3fae063c7')
    version('2.2.9',  sha256='88da749bc2bd75149f0bb6e72eb4a9d74401a54f4508bc730f13cc03c57a17ed')
    version('2.2.8',  sha256='8a8a405c7d659b905757a358dc467f4aa3d7e4dff1d1624779065764d962a246')
    version('2.2.7',  sha256='b8e68435904e1a95661c385f24d6924ed28f416985c6db5a3c7448698ad5fea2')
    version('2.2.6',  sha256='4567cae92f58c1d6ecfc771c456fa95f206d8a5c7c5d6c9010ec688a9fd83750')
    version('2.2.5',  sha256='50bf51f4544f83e69a5a2f564732a2adca63fbe9511430aba12f8d6f3a53ae59')
    version('2.2.4',  sha256='92853137ffff393cc74f829357fdd80ac46a82b46c970e80195db86164cca316')
    version('2.2.3',  sha256='46b8355d90f8cc240555e4e077f223c47b950abeadf3e1af52d6e68d2efc2ff3')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
