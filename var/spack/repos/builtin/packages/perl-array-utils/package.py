# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlArrayUtils(PerlPackage):
    """Small utils for array manipulation"""

    homepage = "http://search.cpan.org/~zmij/Array-Utils/Utils.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/Z/ZM/ZMIJ/Array/Array-Utils-0.5.tar.gz"

    version('0.5', 'ac15e6dce2c7c9d1855ecab9eb00aee6')
