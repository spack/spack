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
    pypi = "tensorpack/tensorpack-0.10.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.10.1', sha256='ae6af59794459de910725d268061f0c86d78f01948f9fd5d7b11dd9770ad71ef')
    version('0.9.8', sha256='bc6566c12471a0f9c0a79acc3d045595b1943af8e423c5b843986b73bfe5425f')

    # FIXME: Add dependencies if required. Only add the python dependency
    # if you need specific versions. A generic python dependency is
    # added implicity by the PythonPackage class.
    depends_on('python@3.3:', when='@0.10.1:', type=('build', 'run'))
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
    depends_on('py-subprocess32', when='@:0.9.8 ^python@:2.999', type=('build', 'run'))
    depends_on('py-functools32',  when='@:0.9.8 ^python@:2.999', type=('build', 'run'))
    #depends_on('py-tensorflow@1.5:1.999', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
