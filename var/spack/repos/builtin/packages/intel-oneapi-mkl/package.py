# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

releases = {
    '2021.1.1': {'irc_id': '17402', 'build': '52'}}


class IntelOneapiMkl(IntelOneApiLibraryPackage):
    """Intel oneAPI MKL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl.html'

    version('2021.1.1', sha256='818b6bd9a6c116f4578cda3151da0612ec9c3ce8b2c8a64730d625ce5b13cc0c', expand=False)

    provides('fftw-api@3')
    provides('scalapack')
    provides('mkl')
    provides('lapack')
    provides('blas')

    def __init__(self, spec):
        self.component_info(dir_name='mkl',
                            components='intel.oneapi.lin.mkl.devel',
                            releases=releases,
                            url_name='onemkl')
        super(IntelOneapiMkl, self).__init__(spec)

    def _join_prefix(self, path):
        return join_path(self.prefix, 'mkl', 'latest', path)

    def _ld_library_path(self):
        dirs = ['lib/intel64']
        for dir in dirs:
            yield self._join_prefix(dir)

    def _library_path(self):
        dirs = ['lib/intel64']
        for dir in dirs:
            yield self._join_prefix(dir)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self._join_prefix('bin/intel64'))
        env.prepend_path('CPATH', self._join_prefix('include'))
        for dir in self._library_path():
            env.prepend_path('LIBRARY_PATH', dir)
        for dir in self._ld_library_path():
            env.prepend_path('LD_LIBRARY_PATH', dir)
        env.set('MKLROOT', join_path(self.prefix, 'mkl', 'latest'))
