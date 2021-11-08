# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install runc
#
# You can edit this file again by typing:
#
#     spack edit runc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


#class Runc(AutotoolsPackage):
class Runc(MakefilePackage):
    """CLI tool for spawning and running containers according to the OCI specification"""

    homepage = "https://github.com/opencontainers/runc"
    url = "https://github.com/opencontainers/runc/archive/refs/tags/v1.0.2.tar.gz"
    maintainers = ["teonnik", "Madeeks"]

    version(
        "1.0.2",
        sha256="6c3cca4bbeb5d9b2f5e3c0c401c9d27bc8a5d2a0db8a2f6a06efd03ad3c38a33",
    )
    version(
        "1.0.1",
        sha256="b25e4273a895af3239bc5e495a007266356038adfb34c4b94b4fc39627a89ad9",
    )

    depends_on('go@1.16:')
    depends_on('libseccomp')

    def edit(self, spec, prefix):
        env['PREFIX'] = prefix
