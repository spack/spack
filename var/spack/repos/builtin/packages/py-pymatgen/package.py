# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPymatgen(PythonPackage):
    """Python Materials Genomics is a robust materials analysis code that
    defines core object representations for structures and molecules with
    support for many electronic structure codes. It is currently the core
    analysis code powering the Materials Project."""

    homepage = "http://www.pymatgen.org/"
    pypi = "pymatgen/pymatgen-4.7.2.tar.gz"

    version('2021.3.9',  sha256='a6f22d69133a48b7801bfd5e6a2878b47b4b4b2ef1a377b87c6c573be14cbf16')
    version('4.7.2', sha256='e439b78cc3833a03963c3c3efe349d8a0e52a1550c8a05c56a89aa1b86657436')
    version('4.6.2', sha256='f34349090c6f604f7d402cb09cd486830b38523639d7160d7fd282d504036a0e')

    # Old versions come pre-cythonized and so don't support newer python versions
    # and 2021.1.1 and newer require Python >= 3.7
    extends('python@:3.6',               ignore='bin/tabulate',  when='@:4.7.2')
    extends('python@3.7:',               ignore='bin/tabulate',  when='@2021.1.1:')

    depends_on('py-setuptools@18.0:', type='build')

    depends_on('py-numpy@1.9:',          type=('build', 'run'))
    depends_on('py-six',                 type=('build', 'run'),  when='@:4.7.2')
    depends_on('py-requests',            type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'),  when='@:4.7.2')
    depends_on('py-monty@0.9.6:',        type=('build', 'run'))
    depends_on('py-scipy@0.14:',         type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.5:', type=('build', 'run'),  when='@:4.7.2')
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-spglib@1.9.8.7:',     type=('build', 'run'))
    depends_on('py-matplotlib@1.5:',     type=('build', 'run'))
    depends_on('py-palettable@2.1.1:',   type=('build', 'run'))

    # dependencies of never versions
    depends_on('py-matplotlib@1.5:',      when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-monty@3.0.2:',         when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-numpy@1.20.1:',        when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-palettable@3.1.1:',    when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-pandas',               when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-plotly@4.5.0:',        when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-ruamel-yaml@0.15.6:',  when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-scipy@1.5.0:',         when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-spglib@1.9.9.44:',     when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-sympy',                when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-uncertainties@3.1.4:', when='@2021.1.1:', type=('build', 'run'))
    depends_on('py-networkx@2.2:',        when='@2021.1.1:', type=('build', 'run'))
