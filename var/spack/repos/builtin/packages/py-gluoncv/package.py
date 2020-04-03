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
#     spack install py-gluoncv
#
# You can edit this file again by typing:
#
#     spack edit py-gluoncv
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGluoncv(PythonPackage):
    """GluonCV provides implementations of state-of-the-art
    (SOTA) deep learning algorithms in computer vision. It aims
    to help engineers, researchers, and students quickly
    prototype products, validate new ideas and learn computer
    vision."""

    homepage = "https://gluon-cv.mxnet.io/"
    url      = "https://github.com/dmlc/gluon-cv/archive/v0.6.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.6.0', sha256='5ac89d73f34d02b2e60595a5cc35f46d0a69376567fae3a9518005dd89161305')

    # FIXME: Add dependencies if required.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    # depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
