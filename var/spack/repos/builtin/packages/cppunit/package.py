# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cppunit(AutotoolsPackage):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url = "http://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"

    version('1.13.2', '0eaf8bb1dcf4d16b12bec30d0732370390d35e6f')
