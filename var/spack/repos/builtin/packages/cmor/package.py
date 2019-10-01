# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cmor(AutotoolsPackage):
    """Climate Model Output Rewriter is used to produce CF-compliant netCDF
    files. The structure of the files created by the library and the metadata
    they contain fulfill the requirements of many of the climate community's
    standard model experiments."""

    homepage = "http://cmor.llnl.gov"
    url = "https://github.com/PCMDI/cmor/archive/3.4.0.tar.gz"

    version('3.4.0', sha256='e700a6d50f435e6ffdedf23bf6832b7d37fe21dc78815e1372f218d1d52bd2cb')
    version('3.3.0', 'cfdeeddab1aedb823e26ec38723bd67e')
    version('3.2.0', 'b48105105d4261012c19cd65e89ff7a6')
    version('3.1.2', '72f7227159c901e4bcf80d2c73a8ce77')

    variant('fortran', default=True, description='Enable Fortran API')
    variant('python', default=False, description='Enable PYTHON support')

    depends_on('uuid')
    depends_on('netcdf')
    depends_on('udunits2')
    depends_on('hdf5@:1.8.19')

    extends('python', when='+python')
    depends_on('python@:2', when='@:3.3 +python')
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

        return extra_args

    def install(self, spec, prefix):
        make('install')

        if '+python' in spec:
            setup_py('install', '--prefix=' + prefix)
