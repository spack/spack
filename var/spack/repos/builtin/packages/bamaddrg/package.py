# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bamaddrg(MakefilePackage):
    """bamaddrg adds read groups to input BAM files,
    streams BAM output on stdout"""

    homepage = "https://github.com/ekg/bamaddrg"
    url      = "https://github.com/ilbiondo/bamaddrg"
    git      = "https://github.com/ilbiondo/bamaddrg.git"

    version('0.1', tag='v0.1')

    depends_on("bamtools", type="build")

    def setup_build_environment(self, env):

        env.set('BAMTOOLS_ROOT', self.spec['bamtools'].prefix)
        env.set('PREFIX', self.prefix)
