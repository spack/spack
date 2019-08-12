# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fyba(AutotoolsPackage):
    """OpenFYBA is the source code release of the FYBA library, distributed
    by the National Mapping Authority of Norway (Statens kartverk) to read
    and write files in the National geodata standard format SOSI."""

    homepage = "https://github.com/kartverket/fyba"
    url      = "https://github.com/kartverket/fyba/archive/4.1.1.tar.gz"

    version('4.1.1', 'ab687582efdef26593796271529a10cb')

    # configure: error: cannot find install-sh or install.sh
    force_autoreconf = True

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # error: macro "min" passed 3 arguments, but takes just 2
    # https://github.com/kartverket/fyba/issues/21
    patch('gcc-6.patch')

    # fatal error: 'sys/vfs.h' file not found
    # https://github.com/kartverket/fyba/issues/12
    patch('vfs-mount-darwin.patch', when='platform=darwin')
