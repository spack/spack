# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install py-blight
#
# You can edit this file again by typing:
#
#     spack edit py-blight
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyBlight(PythonPackage):
    """A catch-all compile-tool wrapper."""

    homepage = "https://github.com/trailofbits/blight"
    pypi     = "blight/blight-0.0.47.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.0.47', sha256='eb4a881adb98e03a0a855b95bfcddb0f4b3ca568b00cb45b571f047ae75c5667')

    # variant('dev')

    depends_on('python@3.7:', type=('build', 'run'))

    # In process of changing build backend after 0.0.47 release.
    depends_on('py-setuptools', type='build')

    # FIXME: Add additional dependencies if required.
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-typing-extensions', type=('build', 'run'))
    depends_on('py-pydantic', type=('build', 'run'))

    def global_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py
        # FIXME: If not needed, delete this function
        options = []
        return options

    def install_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py install
        # FIXME: If not needed, delete this function
        options = []
        return options
