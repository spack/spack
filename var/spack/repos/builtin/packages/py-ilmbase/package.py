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
#     spack install py-ilmbase
#
# You can edit this file again by typing:
#
#     spack edit py-ilmbase
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyIlmbase(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/AcademySoftwareFoundation/openexr/releases/download/v2.3.0/pyilmbase-2.3.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2.3.0', sha256='9c898bb16e7bc916c82bebdf32c343c0f2878fc3eacbafa49937e78f2079a425')

    depends_on('ilmbase')
    depends_on('boost+python')

    # https://github.com/AcademySoftwareFoundation/openexr/issues/336
    parallel = False

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-boost-python-libname=boost_python{0}'.format(spec['python'].version.up_to(2).joined)
        ]

        return args
