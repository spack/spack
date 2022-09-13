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
#     spack install qcat
#
# You can edit this file again by typing:
#
#     spack edit qcat
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Qcat(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/szcompressor/qcat"
    git =      "https://github.com/robertu94/qcat"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['disheng222', 'robertu94']

    version('master', branch="master")

    # FIXME: Add dependencies if required.
    depends_on('zstd')

    def cmake_args(self):
        args = ["-DQCAT_USE_BUNDLES=OFF"]
        return args
