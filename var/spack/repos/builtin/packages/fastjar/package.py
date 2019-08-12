# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fastjar(AutotoolsPackage):
    """Fastjar is a version of Sun's 'jar' utility, written entirely in C."""

    homepage = "http://savannah.nongnu.org/projects/fastjar/"
    url      = "http://download.savannah.gnu.org/releases/fastjar/fastjar-0.98.tar.gz"

    version('0.98', 'd2d264d343d4d0e1575832cc1023c3bf')

    depends_on('zlib')
