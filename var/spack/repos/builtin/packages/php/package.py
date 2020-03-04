# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Php(AutotoolsPackage):
    """PHP is a popular general-purpose scripting language that is especially
    suited to web development."""

    homepage = "https://www.php.net/"
    url      = "https://www.php.net/distributions/php-7.4.3.tar.gz"

    version('7.4.3', sha256='58e421a1dba10da8542a014535cac77a78f0271afb901cc2bd363b881895a9ed')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('libxml2@2.7.6:', type='build')
    depends_on('sqlite@3.7.4:', type='build')
    depends_on('re2c')
