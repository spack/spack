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
#     spack install py-python-xlib
#
# You can edit this file again by typing:
#
#     spack edit py-python-xlib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPythonXlib(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "python-xlib/python-xlib-0.30.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.30', sha256='74131418faf9e7b83178c71d9d80297fbbd678abe99ae9258f5a20cd027acb5f')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('python@2.7,3.3:3.6', type=('build', 'run'))
    depends_on('py-setuptools@30.3.0:', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
