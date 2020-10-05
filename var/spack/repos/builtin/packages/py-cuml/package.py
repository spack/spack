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
#     spack install py-cuml
#
# You can edit this file again by typing:
#
#     spack edit py-cuml
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyCuml(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/rapidsai/cuml/archive/v0.15.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.15.0',  sha256='b6b37c0f370cd4e881fc24083166ee86a934f1b823159ad36fac6457412c79cd')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-numba', type=('build', 'run'))
    depends_on('py-cudf', type=('build', 'run'))
    depends_on('cuda')
    depends_on('py-cupy', type=('build', 'run'))

    for v in ('11.0', '10.2', '10.1'):
        depends_on(
            'libcumlprims@0.15.0-cuda{0}_gdbd0d39_0'.format(v),
            when='^cuda@{0}'.format(v))

    for v in ('@0.15.0',):
        depends_on('libcuml{0}'.format(v), when=v)

    phases = [ 'build_ext', 'install' ]

    build_directory = 'python'

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
