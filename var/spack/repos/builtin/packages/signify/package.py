# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Signify(MakefilePackage):
    """OpenBSD tool to signs and verify signatures on files."""

    homepage = "https://github.com/aperezdc/signify"
    url      = "https://github.com/aperezdc/signify/archive/v23.tar.gz"

    version('23', '0552295572a172740ae8427eb018ede8')

    depends_on('libbsd@0.8:')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PREFIX', self.prefix)
