# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Taskd(CMakePackage):
    """TaskWarrior task synchronization daemon"""

    homepage = "http://www.taskwarrior.org"
    url      = "http://taskwarrior.org/download/taskd-1.1.0.tar.gz"

    version('1.1.0', 'ac855828c16f199bdbc45fbc227388d0')

    depends_on('libuuid')
    depends_on('gnutls')
    depends_on('cmake@2.8:', type='build')

    conflicts('%gcc@:4.7')
