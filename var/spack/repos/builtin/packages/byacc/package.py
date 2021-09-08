# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Byacc(AutotoolsPackage):
    """Berkeley Yacc is an LALR(1) parser generator.  Berkeley Yacc has
    been made as compatible as possible with AT&T Yacc.  Berkeley Yacc
    can accept any input specification that conforms to the AT&T Yacc
    documentation. Specifications that take advantage of undocumented
    features of AT&T Yacc will probably be rejected."""

    homepage = "https://invisible-island.net/byacc/byacc.html"
    url      = "https://invisible-island.net/datafiles/release/byacc-20210808.tar.gz"

    # Check FTP directory ftp://ftp.invisible-island.net/byacc/ to find the latest version
    version('20210808', sha256='cf13bfb6440fb692cf81d20019960303c7c715a1194a3dfd32285e3ed85faa2a')

    provides('yacc')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
