# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import platform


class Vecgeom(CMakePackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
    url = "https://gitlab.cern.ch/api/v4/projects/VecGeom%2FVecGeom/repository/archive.tar.gz?sha=v0.3.rc"

    version('01.00.00', git='https://gitlab.cern.ch/VecGeom/VecGeom.git', tag='v01.00.00')
    version('00.05.00', git='https://gitlab.cern.ch/VecGeom/VecGeom.git', tag='v00.05.00', preferred=True)
    version('0.3.rc', 'c1f5d620f655f3c0610a44e7735203b5')

    variant('cxxstd',
            default='17',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')
    variant('vector',
            default='native',
            values=('sse3', 'sse4.2', 'native'),
            multi=False,
            description='Specify the instruction set for vectorization.')

    depends_on('cmake@3.5:', type='build')

    def cmake_args(self):
        options = [
            '-DBACKEND=Scalar',
            '-DGEANT4=OFF',
            '-DUSOLIDS=ON',
            '-DUSOLIDS_VECGEOM=ON',
            '-DROOT=OFF',
            '-DNO_SPECIALIZATION=ON',
            '-DCMAKE_VERBOSE_MAKEFILE=TRUE']
        options.append('-DCMAKE_CXX_STANDARD={0}'.
                       format(self.spec.variants['cxxstd'].value))
        arch = platform.machine()
        if arch == 'x86_64':
            options.append('-DVECGEOM_VECTOR={0}'.
                           format(self.spec.variants['vector'].value))
        else:
            options.append('-DVECGEOM_VECTOR=' + arch)
        return options
