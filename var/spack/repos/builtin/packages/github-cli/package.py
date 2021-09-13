# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install cli
#
# You can edit this file again by typing:
#
#     spack edit cli
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class GithubCli(Package):
    """gh is GitHub on the command line."""

    homepage = "https://cli.github.com"
    url      = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"

    executables = ['^gh$']

    maintainers = ['underwoo']

    version('2.0.0', sha256='5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426')

    depends_on('go',type='build')

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install', 'prefix=%s' % prefix)
