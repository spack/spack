# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Akantu(CMakePackage):
    """
    Akantu means a little element in Kinyarwanda, a Bantu language. From now
    on it is also an opensource object-oriented Finite Element library which
    has the ambition to be generic and efficient.

    """
    homepage = "https://akantu.ch"
    url      = "https://gitlab.com/akantu/akantu/-/archive/master/akantu-master.tar.bz2"

    maintainers = ['nrichart']

    version('master', git='https://gitlab.com/akantu/akantu.git')

    variant('external_solver', values=('none', 'mumps', 'petsc'),
            default='none', multi=True,
            description="Activates the implicit solver")
    variant('mpi', default=True,
            description="Activates parallel capabilities")
    variant('python', default=True,
            description="Activates python bindings")

    depends_on('boost@:1.67', when='@:3.0.1')
    depends_on('boost')
    depends_on('lapack')
    depends_on('cmake@3.5.1:', type='build')
    depends_on('python', when='+python')
    depends_on('py-numpy', when='+python')
    depends_on('py-scipy', when='+python')
    depends_on('py-pybind11', when='+python')

    depends_on('mumps', when='~mpi external_solver=mumps')
    depends_on('mumps+mpi', when='+mpi external_solver=mumps')
    depends_on('netlib-scalapack', when='+mpi external_solver=mumps')
    depends_on('petsc+double', when='~mpi external_solver=petsc')
    depends_on('petsc+double+mpi', when='+mpi external_solver=petsc')

    depends_on('mpi', when='+mpi')
    depends_on('scotch', when='+mpi')

    extends('python', when='+python')

    conflicts('gcc@:5.3.99')

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DAKANTU_COHESIVE_ELEMENT:BOOL=ON',
            '-DAKANTU_DAMAGE_NON_LOCAL:BOOL=ON',
            '-DAKANTU_HEAT_TRANSFER:BOOL=ON',
            '-DAKANTU_SOLID_MECHANICS:BOOL=ON',
            '-DAKANTU_STRUCTURAL_MECHANICS:BOOL=ON',
            '-DAKANTU_TRACTION_AT_SPLIT_NODE_CONTACT:BOOL=ON',
            '-DAKANTU_PARALLEL:BOOL={0}'.format(
                'ON' if spec.satisfies('+mpi') else 'OFF'),
            '-DAKANTU_PYTHON_INTERFACE:BOOL={0}'.format(
                'ON' if spec.satisfies('+python') else 'OFF'),
        ]

        solvers = []
        if self.spec.satisfies('external_solver=mumps'):
            solvers.append('Mumps')
            args.append('-DMUMPS_DIR:PATH=${0}'.format(spec['mumps'].prefix))
        if self.spec.satisfies('external_solver=petsc'):
            solvers.append('PETSc')

        if len(solvers) > 0:
            args.extend([
                '-DAKANTU_IMPLICIT_SOLVER:STRING={0}'.format(
                    '+'.join(solvers)),
                '-DAKANTU_IMPLICIT:BOOL=ON'])
        else:
            args.append('-DAKANTU_IMPLICIT:BOOL=OFF')

        return args
