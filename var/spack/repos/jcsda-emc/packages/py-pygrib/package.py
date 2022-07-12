# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygrib(PythonPackage):
    """A high-level interface to the ECWMF ECCODES C library for reading GRIB files."""

    homepage = "https://github.com/jswhit/pygrib"
    pypi = "pygrib/pygrib-2.1.4.tar.gz"

    version('2.1.4', sha256='951a409eb3233dd95839dd77c0dbe4d8cbed8f21a4015b1047dec9edec65f545')

    depends_on('eccodes', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-proj', type=('run'))

    # depends_on('python@2.6:2.8,3.2:', type=('build', 'run'), when='@0.9.0')
    # depends_on('python@2.6:2.8,3.3:', type=('build', 'run'), when='@0.10.0')
    # depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@0.13.3')
    # depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@0.17.2')
    # depends_on('python@3.6:', type=('build', 'run'), when='@0.18.0')
