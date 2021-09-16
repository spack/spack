# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtlannot(PythonPackage):
    """Alignment of brain atlas annotations."""

    homepage = 'https://bbpgitlab.epfl.ch/project/proj101/atlas_annotation'
    git = 'git@bbpgitlab.epfl.ch:project/proj101/atlas_annotation.git'

    maintainers = ['EmilieDel', 'Stannislav']

    version('0.1.1', commit='5271681de15f23e1df6f8556405b03218541d241')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')

    # Installation requirements
    depends_on('py-antspyx@0.2.4', type=('run'))
    depends_on('py-atldld@0.2.2', type=('run'))
    # depends_on('py-dvc', type=('run'))
    depends_on('py-matplotlib', type=('run'))
    depends_on('py-numpy', type=('run'))

    # From the "interactive" extra
    depends_on('py-ipython', type=('run'))
    depends_on('py-ipywidgets', type=('run'))
    depends_on('py-nibabel', type=('run'))
    depends_on('py-pynrrd', type=('run'))
    depends_on('py-scipy', type=('run'))
    depends_on('py-toml', type=('run'))
    depends_on('py-tqdm', type=('run'))
