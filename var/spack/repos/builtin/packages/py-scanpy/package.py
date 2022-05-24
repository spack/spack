# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScanpy(PythonPackage):
    """Scanpy is a scalable toolkit for analyzing single-cell gene expression data built jointly with anndata."""

    homepage = "https://scanpy.readthedocs.io/en/stable/"
    pypi     = "scanpy/scanpy-1.9.1.tar.gz"

    version('1.9.1', sha256='00c9a83b649da7e0171c91e9a08cff632102faa760614fd05cd4d1dbba4eb541')

    depends_on('python@3.7:', type='build')
    depends_on('py-setuptools-scm')
    depends_on('py-flit-core@3.4:3')
    depends_on('py-importlib-metadata@0.7:')
    depends_on('py-tomli')
    depends_on('py-packaging')
