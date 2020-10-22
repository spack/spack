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
#     spack install py-visdom
#
# You can edit this file again by typing:
#
#     spack edit py-visdom
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyVisdom(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://files.pythonhosted.org/packages/c9/75/e078f5a2e1df7e0d3044749089fc2823e62d029cc027ed8ae5d71fafcbdc/visdom-0.1.8.9.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.1.8.9', sha256='c73ad23723c24a48156899f78dd76bd4538eba3edf9120b6c65a9528fa677126')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.8:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-tornado', type=('build', 'run'))
    depends_on('py-pyzmq', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-jsonpatch', type=('build', 'run'))
    depends_on('py-websocket-client', type=('build', 'run'))
    depends_on('py-torch@0.3.1:', type=('build', 'run'))
    depends_on('py-pillow', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
