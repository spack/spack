# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nco(AutotoolsPackage):
    """The NCO toolkit manipulates and analyzes data stored in
    netCDF-accessible formats"""

    homepage = "http://nco.sourceforge.net/"
    url      = "https://github.com/nco/nco/archive/4.6.7.tar.gz"

    version('4.7.9', '048f6298bceb40913c3ae433f875dea1e9129b1c86019128e7271d08f274a879')
    version('4.6.7', 'b04c92aa715d3fad3ebebd1fd178ce32')
    version('4.6.6', 'df6fa47aaf6e41adfc0631912a7a341f')
    version('4.6.5', '2afd34a6bb5ff6c7ed39cf40c917b6e4')
    version('4.6.4', '22f4e779d0011a9c0db90fda416c8e45')
    version('4.6.3', '0e1d6616c65ed3a30c54cc776da4f987')
    version('4.6.2', 'b7471acf0cc100343392f4171fb56113')
    version('4.6.1', 'ef43cc989229c2790a9094bd84728fd8')
    version('4.5.5', '9f1f1cb149ad6407c5a03c20122223ce')

    # https://github.com/nco/nco/issues/43
    patch('NUL-0-NULL.patch', when='@:4.6.7')

    variant('doc', default=False, description='Build/install NCO TexInfo-based documentation')

    # See "Compilation Requirements" at:
    # http://nco.sourceforge.net/#bld
    depends_on('netcdf')
    depends_on('antlr@2.7.7+cxx')  # required for ncap2
    depends_on('gsl')              # desirable for ncap2
    depends_on('udunits2')         # allows dimensional unit transformations

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('texinfo@4.12:', type='build', when='+doc')

    conflicts('%gcc@9:', when='@:4.7.8')

    def configure_args(self):
        spec = self.spec
        return ['--{0}-doc'.format('enable' if '+doc' in spec else 'disable')]

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        spack_env.set('NETCDF_INC', spec['netcdf'].prefix.include)
        spack_env.set('NETCDF_LIB', spec['netcdf'].prefix.lib)
        spack_env.set('ANTLR_ROOT', spec['antlr'].prefix)
        spack_env.set('UDUNITS2_PATH', spec['udunits2'].prefix)
