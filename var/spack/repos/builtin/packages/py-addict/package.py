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
#     spack install py-addict
#
# You can edit this file again by typing:
#
#     spack edit py-addict
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyAddict(PythonPackage):
    """addict is a Python module that gives you dictionaries
    whose values are both gettable and settable using
    attributes, in addition to standard item-syntax."""

    homepage = "https://github.com/mewwts/addict"
    url      = "https://github.com/mewwts/addict/archive/v2.2.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2.2.1', sha256='398bba9e7fa25e2ce144c5c4b8ec6208e89b9445869403dfa88ab66ec110fa12')

    # FIXME: Add dependencies if required.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
