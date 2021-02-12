# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sqlitebrowser(CMakePackage):
    """DB Browser for SQLite (DB4S) is a high quality, visual,
    open source tool to create, design, and edit database files
    compatible with SQLite."""

    homepage = "https://sqlitebrowser.org"
    url      = "https://github.com/sqlitebrowser/sqlitebrowser/archive/v3.10.1.tar.gz"

    version('3.12.1', sha256='c1f13a7caeab9c36908d7fd6e46718d5f2bb5d116882c5c6392e7c4b0f8dba0f')
    version('3.12.0', sha256='3f1a1453ed0f4b5b72b0468bf8ee56887eb23d71c2518a449f4eb179471d73d1')
    version('3.11.2', sha256='298acb28878aa712277a1c35c185b07a5a1671cc3e2c6a21b323477b91d486fc')
    version('3.10.1', sha256='36eb53bc75192c687dce298c79f1532c410ce4ecbeeacfb07b9d02a307f16bef')

    msg = 'sqlitebrowser requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%apple-clang@:3.9', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    depends_on('sqlite@3:+functions')
    depends_on('qt@5.5:')
