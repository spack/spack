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


class Lrzip(Package):
    """A compression utility that excels at compressing large files
    (usually > 10-50 MB). Larger files and/or more free RAM means that the
    utility will be able to more effectively compress your files (ie: faster /
    smaller size), especially if the filesize(s) exceed 100 MB. You can either
    choose to optimise for speed (fast compression / decompression) or size,
    but not both."""

    homepage = 'http://lrzip.kolivas.org'
    url      = 'https://github.com/ckolivas/lrzip/archive/v0.630.tar.gz'
    git      = 'https://github.com/ckolivas/lrzip.git'

    version('master', branch='master')
    version('0.630', '3ca7f1d1365aa105089d1fbfc6b0924a')
    version('0.621', '1f07227b39ae81a98934411e8611e341')
    version('0.616', 'd40bdb046d0807ef602e36b1e9782cc0')
    version('0.615', 'f1c01e7f3de07f54d916b61c989dfaf2')

    # depends_on('coreutils')
    depends_on('lzo')
    depends_on('zlib')
    depends_on('bzip2')

    def install(self, spec, prefix):
        set_executable('./autogen.sh')
        autogen = Executable('./autogen.sh')

        configure_args = [
            '--prefix={0}'.format(prefix),
            '--disable-dependency-tracking'
        ]
        autogen(*configure_args)

        make()
        make('install')
