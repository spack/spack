# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hc(MakefilePackage):
    """HC is a global mantle circulation solver following Hager & O'Connell
    (1981) which can compute velocities, tractions, and geoid for simple
    density distributions and plate velocities."""

    homepage = "https://geodynamics.org/cig/software/hc/"
    url      = "https://geodynamics.org/cig/software/hc/hc-1.0.7.tar.gz"

    version('1.0.7', sha256='7499ea76ac4739a9c0941bd57d124fb681fd387c8d716ebb358e6af3395103ed')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def edit(self, spec, prefix):
        # FIXME: Edit the Makefile if necessary
        # FIXME: If not needed delete this function
        # makefile = FileFilter('Makefile')
        # makefile.filter('CC = .*', 'CC = cc')
