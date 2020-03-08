# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Graphblast(CmakePackage, CudaPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage    = "https://www.example.com"
    git         = "https://github.com/gunrock/graphblast.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('master', submodules=True)

    # FIXME: Add dependencies if required.
    depends_on('boost')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        install_tree(self.build_directory, self.prefix)
