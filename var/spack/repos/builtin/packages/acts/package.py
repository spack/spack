# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Acts(CMakePackage):
    """
    A Common Tracking Software (Acts)

    This project contains an experiment-independent set of track reconstruction
    tools. The main philosophy is to provide high-level track reconstruction
    modules that can be used for any tracking detector. The description of the
    tracking detector's geometry is optimized for efficient navigation and
    quick extrapolation of tracks. Converters for several common geometry
    description languages exist. Having a highly performant, yet largely
    customizable implementation of track reconstruction algorithms was a
    primary objective for the design of this toolset. Additionally, the
    applicability to real-life HEP experiments plays major role in the
    development process. Apart from algorithmic code, this project also
    provides an event data model for the description of track parameters and
    measurements.

    Key features of this project include: tracking geometry description which
    can be constructed from TGeo, DD4Hep, or GDML input, simple and efficient
    event data model, performant and highly flexible algorithms for track
    propagation and fitting, basic seed finding algorithms.
    """

    homepage = "http://acts.web.cern.ch/ACTS/"
    git      = "https://github.com/acts-project/acts.git"
    maintainers = ['HadrienG2']

    # Supported Acts versions
    version('master', branch='master')
    version('0.24.0', commit='ef4699c8500bfea59a5fe88bed67fde2f00f0adf')
    version('0.23.0', commit='dc443dd7e663bc4d7fb3c1e3f1f75aaf57ffd4e4')
    version('0.22.1', commit='ca1b8b1645db6b552f44c48d2ff34c8c29618f3a')
    version('0.22.0', commit='2c8228f5843685fc0ae69a8b95dd8fc001139efb')
    version('0.21.0', commit='10b719e68ddaca15b28ac25b3daddce8c0d3368d')
    version('0.20.0', commit='1d37a849a9c318e8ca4fa541ef8433c1f004637b')
    version('0.19.0', commit='408335636486c421c6222a64372250ef12544df6')
    version('0.18.0', commit='d58a68cf75b52a5e0f563bc237f09250aa9da80c')
    version('0.17.0', commit='0789f654ff484b013fd27e5023cf342785ea8d97')
    version('0.16.0', commit='b3d965fe0b8ae335909d79114ef261c6b996773a')
    version('0.15.0', commit='267c28f69c561e64369661a6235b03b5a610d6da')
    version('0.14.0', commit='38d678fcb205b77d60326eae913fbb1b054acea1')
    version('0.13.0', commit='b33f7270ddbbb33050b7ec60b4fa255dc2bfdc88')
    version('0.12.1', commit='a8b3d36e7c6cb86487637589e0eff7bbe626054a')
    version('0.12.0', commit='f9cda77299606d78c889fb1db2576c1971a271c4')
    version('0.11.1', commit='c21196cd6c3ecc6da0f14d0a9ef227a274be584b')
    version('0.11.0', commit='22bcea1f19adb0021ca61b843b95cfd2462dd31d')
    version('0.10.5', commit='b6f7234ca8f18ee11e57709d019c14bf41cf9b19')
    version('0.10.4', commit='42cbc359c209f5cf386e620b5a497192c024655e')
    version('0.10.3', commit='a3bb86b79a65b3d2ceb962b60411fd0df4cf274c')
    version('0.10.2', commit='64cbf28c862d8b0f95232b00c0e8c38949d5015d')
    version('0.10.1', commit='0692dcf7824efbc504fb16f7aa00a50df395adbc')
    version('0.10.0', commit='30ef843cb00427f9959b7de4d1b9843413a13f02')
    version('0.09.5', commit='12b11fe8b0d428ccb8e92dda7dc809198f828672')
    version('0.09.4', commit='e5dd9fbe179201e70347d1a3b9fa1899c226798f')
    version('0.09.3', commit='a8f31303ee8720ed2946bfe2d59e81d0f70e307e')
    version('0.09.2', commit='4e1f7fa73ffe07457080d787e206bf6466fe1680')
    version('0.09.1', commit='69c451035516cb683b8f7bc0bab1a25893e9113d')
    version('0.09.0', commit='004888b0a412f5bbaeef2ffaaeaf2aa182511494')
    version('0.08.2', commit='c5d7568714e69e7344582b93b8d24e45d6b81bf9')
    version('0.08.1', commit='289bdcc320f0b3ff1d792e29e462ec2d3ea15df6')
    version('0.08.0', commit='99eedb38f305e3a1cd99d9b4473241b7cd641fa9')

    # Variants that affect the core Acts library
    variant('benchmarks', default=False, description='Build the performance benchmarks')
    variant('examples', default=False, description='Build the examples')
    variant('integration_tests', default=False, description='Build the integration tests')
    variant('unit_tests', default=False, description='Build the unit tests')

    # Variants that enable / disable Acts plugins
    variant('dd4hep', default=False, description='Build the DD4hep plugin')
    variant('digitization', default=False, description='Build the geometric digitization plugin')
    variant('fatras', default=False, description='Build the FAst TRAcking Simulation package')
    variant('identification', default=False, description='Build the Identification plugin')
    variant('json', default=False, description='Build the Json plugin')
    variant('legacy', default=False, description='Build the Legacy package')
    variant('tgeo', default=False, description='Build the TGeo plugin')

    # Variants that only affect Acts examples for now
    variant('geant4', default=False, description='Build the Geant4-based examples')
    variant('hepmc3', default=False, description='Build the HepMC3-based examples')
    variant('pythia8', default=False, description='Build the Pythia8-based examples')

    # Build dependencies
    depends_on('boost @1.62:1.69.99 +program_options +test', when='@:0.10.3')
    depends_on('boost @1.69: +filesystem +program_options +test', when='@0.10.4:')
    depends_on('cmake @3.11:', type='build')
    depends_on('dd4hep @1.10: +xercesc', when='+dd4hep')
    depends_on('dd4hep @1.10: +geant4 +xercesc', when='+dd4hep +geant4')
    depends_on('eigen @3.2.9:', type='build')
    depends_on('geant4', when='+geant4')
    depends_on('hepmc@3.1:', when='+hepmc3')
    depends_on('heppdt', when='+hepmc3')
    depends_on('intel-tbb', when='+examples')
    depends_on('nlohmann-json @3.2.0:', when='@0.14: +json')
    depends_on('pythia8', when='+pythia8')
    depends_on('root @6.10: cxxstd=14', when='+tgeo @:0.8.0')
    depends_on('root @6.10: cxxstd=17', when='+tgeo @0.8.1:')

    # Some variant combinations do not make sense
    conflicts('+benchmarks', when='@:0.15')
    conflicts('+dd4hep', when='-tgeo')
    conflicts('+examples', when='@:0.22')
    conflicts('+examples', when='-digitization')
    conflicts('+examples', when='-fatras')
    conflicts('+examples', when='-identification')
    conflicts('+examples', when='-json')
    conflicts('+examples', when='-tgeo')
    conflicts('+fatras', when='@:0.15')
    conflicts('+geant4', when='@:0.22')
    conflicts('+geant4', when='-examples')
    conflicts('+hepmc3', when='@:0.22')
    conflicts('+hepmc3', when='-examples')
    conflicts('+pythia8', when='@:0.22')
    conflicts('+pythia8', when='-examples')
    conflicts('+tgeo', when='-identification')

    def cmake_args(self):
        spec = self.spec

        def cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies('+' + spack_variant)
            return "-DACTS_BUILD_{0}={1}".format(cmake_label, enabled)

        def example_cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies('+examples +' + spack_variant)
            return "-DACTS_BUILD_EXAMPLES_{0}={1}".format(cmake_label, enabled)

        integration_tests_label = "INTEGRATIONTESTS"
        unit_tests_label = "UNITTESTS"
        if spec.satisfies('@:0.15.99'):
            integration_tests_label = "INTEGRATION_TESTS"
            unit_tests_label = "TESTS"

        args = [
            cmake_variant("BENCHMARKS", "benchmarks"),
            cmake_variant("DD4HEP_PLUGIN", "dd4hep"),
            cmake_variant("DIGITIZATION_PLUGIN", "digitization"),
            cmake_variant("EXAMPLES", "examples"),
            example_cmake_variant("DD4HEP", "dd4hep"),
            example_cmake_variant("GEANT4", "geant4"),
            example_cmake_variant("HEPMC3", "hepmc3"),
            example_cmake_variant("PYTHIA8", "pythia8"),
            cmake_variant("FATRAS", "fatras"),
            cmake_variant("IDENTIFICATION_PLUGIN", "identification"),
            cmake_variant(integration_tests_label, "integration_tests"),
            cmake_variant("JSON_PLUGIN", "json"),
            cmake_variant(unit_tests_label, "unit_tests"),
            cmake_variant("LEGACY", "legacy"),
            cmake_variant("TGEO_PLUGIN", "tgeo")
        ]

        if 'root' in spec:
            cxxstd = spec['root'].variants['cxxstd'].value
            args.append("-DCMAKE_CXX_STANDARD={0}".format(cxxstd))

        if spec.satisfies('@0.14.0: +json'):
            args.append("-DACTS_USE_BUNDLED_NLOHMANN_JSON=OFF")

        return args
