# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install mutationpp
#
# You can edit this file again by typing:
#
#     spack edit mutationpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class Mutationpp(CMakePackage):
    """Mutation++ is an open-source library originally developed
    at the von Karman Institute for Fluid Dynamics, designed to
    couple with conventional computational fluid dynamics codes
    to provide thermodynamic, transport, chemistry, and energy
    transfer properties associated with subsonic to hypersonic flows."""

    homepage = "https://github.com/mutationpp/Mutationpp"
    url      = "https://github.com/mutationpp/Mutationpp/archive/v0.3.1.tar.gz"

    version('0.3.1', 'a6da2816e145ac9fcfbd8920595b7f65ce7bc8df0bec572b32647720758cbe69')

    variant('fortran', default=True)
    variant('data', default=True)
    variant('examples', default=True)

    def cmake_args(self):
        args = []
        if '+fortran' in self.spec:
            args.append('-DBUILD_FORTRAN_WRAPPER=ON')
        return args

    @run_after('install')
    def install_data(self):
        if '+data' in self.spec and os.path.isdir('data'):
            install_tree('data', join_path(self.prefix, 'data'))

    @run_after('install')
    def install_examples(self):
        if '+examples' in self.spec and os.path.isdir('examples'):
            install_tree('examples', join_path(self.prefix, 'examples'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('MPP_DIRECTORY', self.prefix)
        if os.path.isdir(join_path(self.prefix, 'data')):
            run_env.set('MPP_DATA_DIRECTORY', join_path(self.prefix, 'data'))

    def setup_dependent_environment(self, spack_env, run_env):
        spack_env.set('MPP_DIRECTORY', self.prefix)
        if os.path.isdir(join_path(self.prefix, 'data')):
            spack_env.set('MPP_DATA_DIRECTORY', join_path(self.prefix, 'data'))
