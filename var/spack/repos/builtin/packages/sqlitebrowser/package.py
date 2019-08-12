# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('3.10.1', '66cbe41f9da5be80067942ed3816576c')

    msg = 'sqlitebrowser requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    depends_on('sqlite@3:+functions')
    depends_on('qt@5.5:')
