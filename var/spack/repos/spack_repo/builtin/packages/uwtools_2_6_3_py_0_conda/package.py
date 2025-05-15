# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
#     spack install uwtools-2-6-3-py-0-conda
#
# You can edit this file again by typing:
#
#     spack edit uwtools-2-6-3-py-0-conda
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Uwtools263Py0Conda(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url = "https://anaconda.org/ufs-community/uwtools/2.6.3/download/noarch/uwtools-2.6.3-py_0.conda"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("UNKNOWN", checked_by="github_user1")

    # FIXME: Add proper versions and checksums here.
    # version("1.2.3", md5="0123456789abcdef0123456789abcdef")

    # FIXME: Add dependencies if required.
    # depends_on("foo")

    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make("install")
