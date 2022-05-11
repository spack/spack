# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Cmor(AutotoolsPackage):
    """Climate Model Output Rewriter is used to produce CF-compliant netCDF
    files. The structure of the files created by the library and the metadata
    they contain fulfill the requirements of many of the climate community's
    standard model experiments."""

    homepage = "https://cmor.llnl.gov"
    url = "https://github.com/PCMDI/cmor/archive/3.6.1.tar.gz"

    version('3.6.1', sha256='991035a41424f72ea6f0f85653fc13730eb035e63c7dff6ca740aa7a70976fb4')
    version('3.6.0', sha256='1608904a35106e83d365f27522209c325bd4bfc19d022b1a8abfb12cdf85fe20')
    version('3.5.0', sha256='37ce11332f9adfd4fa7560dfb358d14b300315221614c4a44c7407297103c62a')
    version('3.4.0', sha256='e700a6d50f435e6ffdedf23bf6832b7d37fe21dc78815e1372f218d1d52bd2cb')
    version('3.3.0', sha256='b763707272c470fc6f7077d9c541591a60f9075b52f5f0298eaf2cb2f2fff4d2')
    version('3.2.0', sha256='8d49899549dd4c08197739300d507e6fc2b4a5cfe2bfd3e6b44e8e3eaf79b132')
    version('3.1.2', sha256='ee58b6d405f081e4e0633af931b7992f1a570953b71ece17c01ab9e15889211a')

    variant('fortran', default=True, description='Enable Fortran API')
    variant('python', default=False, description='Enable PYTHON support')

    # older releases require another implementation providing uuid_create()
    # 3.6.1 requires libuuid(only the lib) or util-linux-uuid providing uuid_generate()
    depends_on('hdf5')
    depends_on('hdf5@:1.8.19',    when='@:3.4.0')
    depends_on('ossp-uuid',       when='@:3.4.0')
    depends_on('util-linux-uuid', when='@3.5.0:')
    depends_on('json-c',          when='@3.5.0:')
    depends_on('netcdf-c')
    depends_on('udunits')

    extends('python', when='+python')
    depends_on('python@:2', when='@:3.3 +python', type=('build', 'run'))
    depends_on('py-pip', when='+python', type='build')
    depends_on('py-wheel', when='+python', type='build')
    depends_on('py-numpy', type=('build', 'run'), when='+python')

    @run_before('configure')
    def validate(self):
        if '+fortran' in self.spec and not self.compiler.fc:
            msg = 'cannot build a fortran variant without a fortran compiler'
            raise RuntimeError(msg)

    def configure_args(self):
        extra_args = ['--disable-debug']

        if '+fortran' in self.spec:
            extra_args.append('--enable-fortran')
        else:
            extra_args.append('--disable-fortran')

        if '+python' in self.spec:
            extra_args.append('--with-python={0}'.format(self.spec['python'].prefix))

        return extra_args

    def check(self):
        """tests need downloaded files, testcases have manual instructions for that."""
        pass

    def install(self, spec, prefix):
        make('install')

        if '+python' in spec:
            args = std_pip_args + ['--prefix=' + prefix, '.']
            pip(*args)
