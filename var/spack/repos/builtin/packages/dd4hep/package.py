# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dd4hep(CMakePackage):
    """DD4hep is a software framework for providing a complete solution for
       full detector description (geometry, materials, visualization, readout,
       alignment, calibration, etc.) for the full experiment life cycle
       (detector concept development, detector optimization, construction,
       operation). It offers a consistent description through a single source
       of detector information for simulation, reconstruction, analysis, etc.
       It distributed under the LGPLv3 License."""

    homepage = "https://dd4hep.web.cern.ch/dd4hep/"
    git      = "https://github.com/AIDASoft/DD4hep.git"

    version('master', branch='master')
    version('1.11.0', commit='280c7d748d56a704699408ac8e57815d029b169a')
    version('1.10.0', commit='9835d1813c07d9d5850d1e68276c0171d1726801')

    # Workarounds for various TBB issues in DD4hep v1.11
    # See https://github.com/AIDASoft/DD4hep/pull/613 .
    patch('tbb-workarounds.patch', when='@1.11.0')

    variant('xercesc', default=False, description="Enable 'Detector Builders' based on XercesC")
    variant('geant4', default=False, description="Enable the simulation part based on Geant4")
    variant('testing', default=False, description="Enable and build tests")

    depends_on('cmake @3.12:', type='build')
    depends_on('boost @1.49:')
    depends_on('root @6.08: +gdml +math +opengl +python +x')
    depends_on('python')
    depends_on('xerces-c', when='+xercesc')
    depends_on('geant4@10.2.2:', when='+geant4')

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec['root'].variants['cxxstd'].value
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DDD4HEP_USE_XERCESC={0}".format(spec.satisfies('+xercesc')),
            "-DDD4HEP_USE_GEANT4={0}".format(spec.satisfies('+geant4')),
            "-DBUILD_TESTING={0}".format(spec.satisfies('+testing')),
            "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
            "-DBoost_NO_BOOST_CMAKE=ON",
            "-DPYTHON_EXECUTABLE={0}".format(spec['python'].command.path),
        ]
        return args
