# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Log4cplus(CMakePackage):
    """log4cplus is a simple to use C++ logging API
    providing thread-safe, flexible, and arbitrarily
    granular control over log management and configuration."""

    homepage = "https://sourceforge.net/projects/log4cplus/"
    url      = "https://download.sourceforge.net/project/log4cplus/log4cplus-stable/2.0.1/log4cplus-2.0.1.tar.bz2"

    version('2.0.1', 'ec01c03241ebd31127a44d1880830d8f')
    version('1.2.1', 'e4e6c38b065b70b5d6efc238a5106bc9')
    version('1.2.0', 'e250f0f431c0723f8b625323e7b6465d')
