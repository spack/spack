# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythran(PythonPackage):
    """Ahead of Time compiler for numeric kernels."""

    homepage = "https://github.com/serge-sans-paille/pythran"
    pypi     = "pythran/pythran-0.9.11.tar.gz"

    version('0.9.11', sha256='a317f91e2aade9f6550dc3bf40b5caeb45b7e012daf27e2b3e4ad928edb01667')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-ply@3.4:', type=('build', 'run'))
    depends_on('py-networkx@2:', type=('build', 'run'))
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-gast@0.4.0:0.4.999', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-beniget@0.3.0:0.3.999', type=('build', 'run'))
