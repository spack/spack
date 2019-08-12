# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libelf(AutotoolsPackage):
    """libelf lets you read, modify or create ELF object files in an
       architecture-independent way. The library takes care of size
       and endian issues, e.g. you can process a file for SPARC
       processors on an Intel-based system. Note: libelf is no longer
       maintained and packages that depend on libelf should migrate to
       elfutils."""

    # The original homepage no longer exists, but the tar file is
    # archived at fossies.org.
    # homepage = "http://www.mr511.de/software/english.html"

    homepage = "https://directory.fsf.org/wiki/Libelf"
    url      = "https://fossies.org/linux/misc/old/libelf-0.8.13.tar.gz"

    version('0.8.13', '4136d7b4c04df68b686570afa26988ac')
    # version('0.8.12', 'e21f8273d9f5f6d43a59878dc274fec7')

    provides('elf@0')

    def configure_args(self):
        args = ["--enable-shared",
                "--disable-dependency-tracking",
                "--disable-debug"]
        return args

    def install(self, spec, prefix):
        make('install', parallel=False)
