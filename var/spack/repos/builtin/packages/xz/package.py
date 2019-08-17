# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xz(AutotoolsPackage):
    """XZ Utils is free general-purpose data compression software with
    high compression ratio. XZ Utils were written for POSIX-like systems,
    but also work on some not-so-POSIX systems. XZ Utils are the successor
    to LZMA Utils."""

    homepage = "http://tukaani.org/xz/"
    url      = "http://tukaani.org/xz/xz-5.2.4.tar.bz2"
    list_url = "http://tukaani.org/xz/old.html"

    version('5.2.4', 'b3264b15ab1db04c8c428dc81838d4eb')
    version('5.2.3', '1592e7ca3eece099b03b35f4d9179e7c')
    version('5.2.2', 'f90c9a0c8b259aee2234c4e0d7fd70af')
    version('5.2.0', '867cc8611760240ebf3440bd6e170bb9')

    @property
    def libs(self):
        return find_libraries(['liblzma'], root=self.prefix, recursive=True)
