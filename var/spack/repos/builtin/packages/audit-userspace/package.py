# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AuditUserspace(AutotoolsPackage):
    """Linux audit userspace"""

    homepage = "https://github.com/linux-audit/audit-userspace"
    url      = "https://github.com/linux-audit/audit-userspace/archive/v2.8.5.tar.gz"

    version('3.0.1', sha256='82e5d684c56c172977de6adb8ed0fb54218cc92f1f05e8303e13868e065886df')
    version('3.0',   sha256='fc57db8cf3e7ebb9f871d523832694b6667a990bcbf41d854248f391e40c0a91')
    version('2.8.5', sha256='835ffdd65056ba0c26509dbf48882713b00dbe70e1d8cf25d538501136c2e3e9')
    version('2.8.4', sha256='089dfdceb38edf056202a6de4892fd0c9aaa964c08bd7806c5d0c7c33f09e18d')
    version('2.8.3', sha256='c239e3813b84bc264aaf2f796c131c1fe02960244f789ec2bd8d88aad4561b29')
    version('2.8.2', sha256='0a312a8487190d97715d46abb30aa2abd464b55f21d5c2d24428baa320ee4ce2')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('openldap')
    depends_on('swig')
