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
#     spack install py-mmcv
#
# You can edit this file again by typing:
#
#     spack edit py-mmcv
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyMmcv(PythonPackage):
    """MMCV is a foundational python library for computer
    vision research and supports many research projects in
    MMLAB, such as MMDetection and MMAction."""

    homepage = "https://mmcv.readthedocs.io/en/latest/"
    url      = "https://github.com/open-mmlab/mmcv/archive/v0.5.1.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.5.1', sha256='7c5ad30d9b61e44019e81ef46c406aa85dd08b5d0ba12ddd5cdc9c445835a55e')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-addict', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('opencv+python', type=('build', 'run'))
    depends_on('py-cython', type='build')

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
