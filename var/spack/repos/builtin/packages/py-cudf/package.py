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
#     spack install py-cudf
#
# You can edit this file again by typing:
#
#     spack edit py-cudf
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyCudf(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/rapidsai/cudf/archive/v0.15.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.15.0',  sha256='57b8036134368daa8a967eae971ee121cdc58c8678a03eba1358ed2b927dc16e')

    build_directory = 'python/cudf'

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))
    depends_on('python@3.6:3.7', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numba@0.40.0:', type=('build', 'run'))
    depends_on('py-numpy@1.14.4:', type=('build', 'run'))
    depends_on('py-pyarrow+cuda', type=('build', 'run'))
    depends_on('py-pandas@0.23.4:', type=('build', 'run'))
    depends_on('py-rmm', type=('build', 'run'))
    depends_on('cuda@10:')
    
    for v in ('@0.15.0',):
        depends_on('libcudf' + v, when=v)

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
