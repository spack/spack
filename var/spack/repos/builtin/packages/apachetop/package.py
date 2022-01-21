# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Apachetop(AutotoolsPackage):
    """ApacheTop watches a logfile generated by Apache (in standard common or
    combined logformat, and generates human-parsable output in realtime.)
    See the INSTALL file for ./configure options (there's a few newly added
    since v0.11)"""

    homepage = "https://github.com/tessus/apachetop"
    url      = "https://github.com/tessus/apachetop/archive/0.19.7.tar.gz"

    version('0.19.7', sha256='88abf58ee5d7882e4cc3fa2462865ebbf0e8f872fdcec5186abe16e7bff3d4a5')
    version('0.18.4', sha256='1cbbfd1bf12275fb21e0cb6068b9050b2fee8c276887054a015bf103a1ae9cc6')
    version('0.17.4', sha256='892ed3b83b45eb38811e74d068089b1e8c34707787f240ce133d8c93198d7ff0')
    version('0.15.6', sha256='7343caeb1adab795439b7be9cf47ce6049751ae948537d5f27251c075264801a')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('readline')
