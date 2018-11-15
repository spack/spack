# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class PyCffi(PythonPackage):
    """Foreign Function Interface for Python calling C code"""
    homepage = "http://cffi.readthedocs.org/en/latest/"
    url      = "https://pypi.io/packages/source/c/cffi/cffi-1.10.0.tar.gz"

    import_modules = ['cffi']

    version('1.11.5', 'ac8492f4ad952360737413e82d661908')
    version('1.10.0', '2b5fa41182ed0edaf929a789e602a070')
    version('1.1.2',  'ca6e6c45b45caa87aee9adc7c796eaea')

    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-pycparser', type=('build', 'run'))
    depends_on('libffi')

    def setup_environment(self, spack_env, run_env):
        # This sets the compiler (and flags) that distutils will use
        # to create the final shared library.  It will use the
        # compiler specified by the environment variable 'CC' for all
        # other compilation.  We are setting the 'LDSHARED" to the
        # spack compiler wrapper plus a few extra flags necessary for
        # building the shared library.
        if not sys.platform == 'darwin':
            spack_env.set('LDSHARED', "{0} -shared -pthread".format(spack_cc))
