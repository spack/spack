# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Reprimand(MesonPackage):
    """RePrimAnd is a support library for numerical simulations of general
    relativistic magnetohydrodynamics. If provides methods for recovering
    primitive variables like pressure and velocity from the variables evolved
    in quasi-conservative formulations. Further, it provides a general
    framework for handling matter equations of state."""

    homepage = "https://www.atlas.aei.uni-hannover.de/holohome/wolfgang.kastaun/doc/reprimand/latest/index.html"
    url      = "https://github.com/wokast/RePrimAnd/archive/refs/tags/v1.3.tar.gz"

    maintainers = ['eschnett']

    version('develop', git='https://github.com/wokast/RePrimAnd', branch='public')
    version('1.3', sha256='8e9f05b1f065a876d1405562285a9f64d1b31c4a436d5a6bb1f023212b40314e')

    # Add missing #include statments; see
    # <https://github.com/wokast/RePrimAnd/issues/3>
    patch('include.patch', when='@1.3')

    variant('python', default=False, description='Enable Python bindings')
    variant('shared', default=True, description='Build shared library')

    depends_on('boost')
    depends_on('gsl')
    depends_on('hdf5')
    depends_on('python', when='+python')
    depends_on('py-matplotlib', when='+python')
    depends_on('py-pybind11 @2.6.0:', when='+python')

    extends('python', when='+python')

    def setup_build_environment(self, env):
        env.set('CXXFLAGS', self.compiler.cxx11_flag)
        env.set('BOOST_ROOT', self.spec['boost'].prefix)

    def meson_args(self):
        args = [
            '-Dbuild_documentation=false',
            '-Dbuild_python_api={0}'.format(
                str('+python' in self.spec).lower()),
        ]
        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(
            "libRePrimAnd*", root=self.prefix, shared=shared, recursive=True
        )
