# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libmad(AutotoolsPackage):
    """MAD is a high-quality MPEG audio decoder."""

    homepage = "https://www.underbit.com/products/mad/"
    url      = "https://download.sourceforge.net/project/mad/libmad/0.15.1b/libmad-0.15.1b.tar.gz"

    version('0.15.1b', sha256='bbfac3ed6bfbc2823d3775ebb931087371e142bb0e9bb1bee51a76a6e0078690')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    patch('libmad-0.15.1b.patch')

    force_autoreconf = True
