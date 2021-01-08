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
#     spack install py-tensorpack
#
# You can edit this file again by typing:
#
#     spack edit py-tensorpack
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyTensorpack(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "https://github.com/tensorpack/tensorpack/archive/v0.10.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.10.1', sha256='8304bdf03ce88ecb08da9ae0b136c572b75695ad2b6cd552489f8a22bfea14c3')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    # depends_on('python@2.X:2.Y,3.Z:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on("py-numpy@1.14:", type=('build', 'run'))
    depends_on("py-six", type=('build', 'run'))
    depends_on("py-termcolor@1.1:", type=('build', 'run'))
    depends_on("py-tabulate@0.7.7:", type=('build', 'run'))
    depends_on("py-tqdm@4.29.0.1:", type=('build', 'run'))
    depends_on("py-msgpack@0.5.2:", type=('build', 'run'))
    depends_on("py-msgpack-numpy@0.4.4.2:", type=('build', 'run'))
    depends_on("py-pyzmq@16:", type=('build', 'run'))
    depends_on("py-psutil@5:", type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
