# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PySymengine(PythonPackage):
    """Python wrappers for SymEngine, a symbolic manipulation library."""

    homepage = "https://github.com/symengine/symengine.py"
    pypi = "symengine/symengine-0.2.0.tar.gz"
    git      = "https://github.com/symengine/symengine.py.git"

    version('master', branch='master')
    # pypi source doesn't have necessary files in cmake directory
    version('0.8.1',
            url='https://github.com/symengine/symengine.py/archive/refs/tags/v0.8.1.tar.gz',
            sha256='02fe79e6d5e9b39a1d4e6fee05a2c1d1b10fd032157c7738ed97e32406ffb087')
    version('0.2.0', sha256='78a14aea7aad5e7cbfb5cabe141581f9bba30e3c319690e5db8ad99fdf2d8885')

    # Build dependencies
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'), when='@0.2.0')
    depends_on('python@3.6:3', type=('build', 'run'), when='@0.8.1:')
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.19.1:', type='build', when='@0.2.0')
    depends_on('py-cython@0.29.24:', type='build', when='@0.8.1:')
    depends_on('cmake@2.8.12:',      type='build')
    depends_on('symengine@0.2.0', when='@0.2.0')
    depends_on('symengine@0.8.1', when='@0.8.1')

    def install_options(self, spec, prefix):
        return ['--symengine-dir={0}'.format(spec['symengine'].prefix)]
