# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatasets(PythonPackage):
    """Datasets is a lightweight library providing two main
    features: one-line dataloaders for many public datasets and
    efficient data pre-processing."""

    homepage = "https://github.com/huggingface/datasets"
    pypi     = "datasets/datasets-1.8.0.tar.gz"

    version('1.8.0', sha256='d57c32bb29e453ee7f3eb0bbca3660ab4dd2d0e4648efcfa987432624cab29d3')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.17:', type=('build', 'run'))
    depends_on('py-pyarrow@1.0.0:3+parquet', type=('build', 'run'))
    depends_on('py-dill', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-requests@2.19:', type=('build', 'run'))
    depends_on('py-tqdm@4.27:4.49', type=('build', 'run'))
    depends_on('py-dataclasses', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-xxhash', type=('build', 'run'))
    depends_on('py-multiprocess', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='^python@:3.7', type=('build', 'run'))
    depends_on('py-huggingface-hub@:0.0', type=('build', 'run'))
    depends_on('py-packaging', type=('build', 'run'))

    depends_on('py-fsspec@:0.8.0', when='^python@:3.7', type=('build', 'run'))
    depends_on('py-fsspec', when='^python@3.8:', type=('build', 'run'))
