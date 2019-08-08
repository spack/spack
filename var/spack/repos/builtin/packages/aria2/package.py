# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install aria2
#
# You can edit this file again by typing:
#
#     spack edit aria2
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Aria2(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://github.com/aria2/aria2/releases/download/release-1.34.0/aria2-1.34.0.tar.gz"

    version('1.34.0', sha256='ec4866985760b506aa36dc9021dbdc69551c1a647823cae328c30a4f3affaa6c')

    # FIXME: Add dependencies if required.
    depends_on('libxml2')
    depends_on('libssh2')
    depends_on('libgcrypt')
    depends_on('zlib')
    depends_on('cares')
    depends_on('sqlite')
