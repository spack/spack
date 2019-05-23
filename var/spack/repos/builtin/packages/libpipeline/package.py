# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpipeline(AutotoolsPackage):
    """libpipeline is a C library for manipulating pipelines of subprocesses
    in a flexible and convenient way."""

    homepage = "http://libpipeline.nongnu.org/"
    url      = "http://git.savannah.nongnu.org/cgit/libpipeline.git/snapshot/libpipeline-1.4.2.tar.gz"

    version('1.4.2', '30cec7bcd6fee723adea6a54389f3da2')

    depends_on('pkgconfig', type='build')
    depends_on('check', type='test')
