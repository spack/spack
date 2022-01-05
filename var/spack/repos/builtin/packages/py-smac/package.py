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
#     spack install py-smac
#
# You can edit this file again by typing:
#
#     spack edit py-smac
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PySmac(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "smac/smac-1.1.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.1.1', sha256='7b8c14c53384b32feb357b9f918a9b023cb01cbda2033e69125dee69ec0bd5b1')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7.1:', type=('build', 'run'))
    depends_on('py-scipy@1.7.0:', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-pynisher@0.4.1:', type=('build', 'run'))
    depends_on('py-configspace@0.4.14:0.4.999', type=('build', 'run'))
    depends_on('py-joblib', type=('build', 'run'))
    depends_on('py-scikit-learn@0.22.0:', type=('build', 'run'))
    depends_on('py-pyrfr@0.8.0:', type=('build', 'run'))
    depends_on('py-dask', type=('build', 'run'))
    depends_on('py-distributed', type=('build', 'run'))
    depends_on('py-emcee@3.0.0:', type=('build', 'run'))
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
