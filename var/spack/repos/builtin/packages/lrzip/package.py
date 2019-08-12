# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
