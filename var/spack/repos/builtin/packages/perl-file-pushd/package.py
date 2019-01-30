# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFilePushd(PerlPackage):
    """Change directory temporarily for a limited scope"""

    homepage = "http://search.cpan.org/~dagolden/File-pushd-1.014/lib/File/pushd.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/File-pushd-1.014.tar.gz"

    version('1.014', '09c03001fb653c35663842191e315f5f')
