# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAnndata(PythonPackage):
    """anndata is a Python package for handling annotated data matrices 
    in memory and on disk, positioned between pandas and xarray."""

    homepage = "https://www.example.com"
    pypi     = "anndata/anndata-0.8.0.tar.gz"

    version('0.8.0', sha256='94d2cc6f76c0317c0ac28564e3092b313b7ad19c737d66701961f3e620b9066e')

    depends_on('python@3.7:', type='build')
    depends_on('py-setuptools-scm', type=('build', 'run'))
    depends_on('py-flit-core@3.4:3', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.7:', type=('build', 'run'))
