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
#     spack install py-datasets
#
# You can edit this file again by typing:
#
#     spack edit py-datasets
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyDatasets(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    pypi     = "datasets/datasets-1.8.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('1.8.0', sha256='d57c32bb29e453ee7f3eb0bbca3660ab4dd2d0e4648efcfa987432624cab29d3')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.17:', type=('build', 'run'))
    depends_on('py-pyarrow@1.0.0:3.999+parquet', type=('build', 'run'))
    depends_on('py-dill', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-requests@2.19:', type=('build', 'run'))
    depends_on('py-tqdm@4.27:4.49.999', type=('build', 'run'))
    depends_on('py-dataclasses', when='^python@:3.6.999', type=('build', 'run'))
    depends_on('py-xxhash', type=('build', 'run'))
    depends_on('py-multiprocess', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='^python@:3.7.999', type=('build', 'run'))
    depends_on('py-huggingface-hub@:0.0.999', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))

    depends_on('py-fsspec@:0.8.0', when='^python@:3.7.999', type=('build', 'run'))
    depends_on('py-fsspec', when='^python@3.8:', type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
