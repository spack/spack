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
#     spack install apbs
#
# You can edit this file again by typing:
#
#     spack edit apbs
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Apbs(AutotoolsPackage):
    """APBS solves the equations of continuum electrostatics
    for large biomolecular assemblages."""

    homepage = "http://www.poissonboltzmann.org/"
    url      = "https://downloads.sourceforge.net/project/apbs/apbs/apbs-1.3.0/apbs-1.3-source.tar.gz"

    # Working around race condition
    parallel = False

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # Version 1.4.2.1 uses cmake. Commented out pending resolution of
    # https://github.com/spack/spack/pull/12941
    # version('1.4.2.1', sha256='aa3de78394ccfdbc29115f07fb005480603a4884628b8f82c9e38d93889dc2be',
    #         url="https://downloads.sourceforge.net/project/apbs/apbs/apbs-1.4.2/apbs-1.4.2.1-source.tar.gz" )
    version('1.3', sha256='5fa5b597f7d5a3d9bb55429ec4fefc69e7d0f918d568c3c4a288088c0fde9ef2')

    variant('python', default=False, description='Build with python wrappers')

    depends_on('python@:2.9999', when='+python')
    depends_on('maloc@:1.4')

    def configure_args(self):
        spec = self.spec
        args = []

        args.append('--disable-maloc-rebuild')

        if '+python' in spec:
            args.append('--enable-python')
        else:
            args.append('--disable-python')

        return args
