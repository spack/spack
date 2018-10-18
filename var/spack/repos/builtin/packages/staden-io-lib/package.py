# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class StadenIoLib(AutotoolsPackage):
    """Io_lib is a library for reading/writing various bioinformatics
       file formats."""

    homepage = "http://staden.sourceforge.net/"
    url      = "https://sourceforge.net/projects/staden/files/io_lib/1.14.8/io_lib-1.14.8.tar.gz/download"

    version('1.14.8', 'fe5ee6aaec8111a5bc3ac584a0c0c0c7')

    depends_on('zlib')
