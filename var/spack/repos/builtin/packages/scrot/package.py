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
#     spack install scrot
#
# You can edit this file again by typing:
#
#     spack edit scrot
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Scrot(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/resurrecting-open-source-projects/scrot/archive/refs/tags/1.5.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.5', sha256='87afba3998aac097f13231f3b0452c21188bf4b5cc6ac0747693a1da1a0ae40f')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('autoconf-archive', type='build')
    depends_on('automake', type='build')
    depends_on('giblib')
    depends_on('imlib2')
    depends_on('libtool')
    depends_on('libxcomposite')
    depends_on('libxfixes')

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
