# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    depends_on('gmt@4.2.1:4.999')
    depends_on('netcdf')

    # Build phase fails in parallel with the following error messages:
    # /usr/bin/ld: cannot find -lrick
    # /usr/bin/ld: cannot find -lhc
    # /usr/bin/ld: cannot find -lggrd
    parallel = False

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GMTHOME', self.spec['gmt'].prefix)
        spack_env.set('NETCDFHOME', self.spec['netcdf'].prefix)
        spack_env.set('HC_HOME', self.prefix)
        spack_env.unset('ARCH')

    def install(self, spec, prefix):
        # Most files are installed during the build stage.
        # Manually install header files as well.
        for header in find('.', '*.h'):
            install(header, prefix.include)
