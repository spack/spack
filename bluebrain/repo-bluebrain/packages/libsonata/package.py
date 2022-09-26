# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsonata(CMakePackage):
    """
    `libsonata` provides C++ API for reading SONATA Nodes / Edges

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"
    url = "https://pypi.io/packages/source/l/libsonata/libsonata-0.1.14.tar.gz"

    version('develop', branch='master')
    version('0.1.14', sha256='a5c75df1c3ef6fac10d92fb6781643e0834e5c35debe77693686dab8bfcf221f')
    version('0.1.13', sha256='8263938e49b501c477f626b4c25e0c74e91152268830c69aabc96eeb263c6eea')
    version('0.1.12', sha256='f0fa0f3b129d28e41b337ce2c39c3604990752de8e485327ec9df3bf0360e9c1')
    version('0.1.11', sha256='95f302818971fec3f19ef18febd5c31c580490692138c8e4fe3534104d88b5e0')
    version('0.1.10', sha256='7ef9f911f7ea31da5ff5306d8372ec194d223850aede0878ac2a921ce049bbb2')

    variant('mpi', default=True, description="Enable MPI backend")

    depends_on('cmake@3.3:', type='build')
    depends_on('py-setuptools-scm', type='build', when='@0.1:')
    depends_on('fmt@4.0:')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('catch2', when='@0.1.3:')
    # Version restriction guessed from old deployment
    #
    # No `when` clause, as clingo will penalize new versions with the
    # version penalty from `nlohmann-js` then :(
    depends_on('nlohmann-json@:3.9.1')

    def cmake_args(self):
        result = [
            '-DEXTLIB_FROM_SUBMODULES=OFF',
            '-DSONATA_TESTS=OFF',
        ]
        if not self.spec.satisfies('@develop'):
            result.append('-DSONATA_CXX_WARNINGS:BOOL=OFF')
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicc
                ),
                '-DCMAKE_CXX_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicxx
                ),
            ])
        return result
