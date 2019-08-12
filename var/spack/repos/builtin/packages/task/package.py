# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Task(CMakePackage):
    """Feature-rich console based todo list manager"""
    homepage = "http://www.taskwarrior.org"
    url      = "http://taskwarrior.org/download/task-2.4.4.tar.gz"

    version('2.5.1', 'bcd984a00d6d1eb6b40faf567419f784')
    version('2.4.4', '517450c4a23a5842df3e9905b38801b3')

    depends_on('cmake@2.8:', type='build')
    depends_on('gnutls')
    depends_on('libuuid')

    conflicts('%gcc@:4.7')
