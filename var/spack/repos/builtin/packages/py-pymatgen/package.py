# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymatgen(PythonPackage):
    """Python Materials Genomics is a robust materials analysis code that
    defines core object representations for structures and molecules with
    support for many electronic structure codes. It is currently the core
    analysis code powering the Materials Project."""

    homepage = "http://www.pymatgen.org/"
    url      = "https://pypi.io/packages/source/p/pymatgen/pymatgen-4.7.2.tar.gz"

    version('4.7.2', '9c3a6e8608671c216e4ef89778646fd6')
    version('4.6.2', '508f77fdc3e783587348e93e4dfed1b8')

    extends('python', ignore='bin/tabulate')

    depends_on('py-setuptools@18.0:', type='build')

    depends_on('py-numpy@1.9:',          type=('build', 'run'))
    depends_on('py-six',                 type=('build', 'run'))
    depends_on('py-requests',            type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'))
    depends_on('py-monty@0.9.6:',        type=('build', 'run'))
    depends_on('py-scipy@0.14:',         type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.5:', type=('build', 'run'))
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-spglib@1.9.8.7:',     type=('build', 'run'))
    depends_on('py-matplotlib@1.5:',     type=('build', 'run'))
    depends_on('py-palettable@2.1.1:',   type=('build', 'run'))
