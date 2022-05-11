# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Dd4hep(CMakePackage):
    """DD4hep is a software framework for providing a complete solution for
       full detector description (geometry, materials, visualization, readout,
       alignment, calibration, etc.) for the full experiment life cycle
       (detector concept development, detector optimization, construction,
       operation). It offers a consistent description through a single source
       of detector information for simulation, reconstruction, analysis, etc.
       It distributed under the LGPLv3 License."""

    homepage = "https://dd4hep.web.cern.ch/dd4hep/"
    url      = "https://github.com/AIDASoft/DD4hep/archive/v01-12-01.tar.gz"
    git      = "https://github.com/AIDASoft/DD4hep.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    tags = ['hep']

    version('master', branch='master')
    version('1.20.2', sha256='3dab7a300f749452791e160db9394180b65533e91b1b628e568da72ca79b211a')
    version('1.20.1', sha256='18c18a125583c39cb808c602e052cc2379aa3a8029aa78dbb40bcc31f1deb798')
    version('1.20', sha256='cf6af0c486d5c84e8c8a8e40ea16cec54d4ed78bffcef295a0eeeaedf51cab59')
    version('1.19', sha256='d2eccf5e8402ba7dab2e1d7236e12ee4db9b1c5e4253c40a140bf35580db1d9b')
    version('1.18', sha256='1e909a42b969dfd966224fa8ab1eca5aa05136baf3c00a140f2f6d812b497152')
    version('1.17', sha256='036a9908aaf1e13eaf5f2f43b6f5f4a8bdda8183ddc5befa77a4448dbb485826')
    version('1.16.1', sha256='c8b1312aa88283986f89cc008d317b3476027fd146fdb586f9f1fbbb47763f1a')
    # versions older than 1.16.1 are no longer supported
    # (they need several patches like https://github.com/AIDASoft/DD4hep/pull/796)
    version('1.16', sha256='ea9755cd255cf1b058e0e3cd743101ca9ca5ff79f4c60be89f9ba72b1ae5ec69', deprecated=True)
    version('1.15', sha256='992a24bd4b3dfaffecec9d1c09e8cde2c7f89d38756879a47b23208242f4e352', deprecated=True)
    version('1.14.1', sha256='5b5742f1e23c2b36d3174cca95f810ce909c0eb66f3d6d7acb0ba657819e6717', deprecated=True)
    version('1.14', sha256='b603aa3c0db8dda392253aa71fa4a0f0c3c9715d47df0b895d45c1e8849f4895', deprecated=True)
    version('1.13.1', sha256='83fa70cd74ce93b2f52f098388dff58d179f05ace5b50aea3f408bb8abf7cb73', deprecated=True)
    version('1.13', sha256='0b1f9d902ebe21a9178c1e41204c066b29f68c8836fd1d03a9ce979811ddb295', deprecated=True)
    version('1.12.1', sha256='85e8c775ec03c499ce10911e228342e757c81ce9ef2a9195cb253b85175a2e93', deprecated=True)
    # these version won't build with +ddcad as the subpackage doesn't exit yet
    version('1.12', sha256='133a1fb8ce0466d2482f3ebb03e60b3bebb9b2d3e33d14ba15c8fbb91706b398', deprecated=True)
    version('1.11.2', sha256='96a53dd26cb8df11c6dae54669fbc9cc3c90dd47c67e07b24be9a1341c95abc4', deprecated=True)
    version('1.11.1', sha256='d7902dd7f6744bbda92f6e303ad5a3410eec4a0d2195cdc86f6c1167e72893f0', deprecated=True)
    version('1.11', sha256='25643296f15f9d11ad4ad550b7c3b92e8974fc56f1ee8e4455501010789ae7b6', deprecated=True)
    version('1.10', sha256='1d6b5d1c368dc8bcedd9c61b7c7e1a44bad427f8bd34932516aff47c88a31d95', deprecated=True)

    generator = 'Ninja'

    # Workarounds for various TBB issues in DD4hep v1.11
    # See https://github.com/AIDASoft/DD4hep/pull/613 .
    patch('tbb-workarounds.patch', when='@1.11')
    patch('tbb2.patch', when='@1.12.1')
    # Workaround for failing build file generation in some cases
    # See https://github.com/spack/spack/issues/24232
    patch('cmake_language.patch', when='@:1.17')

    # variants for subpackages
    variant('ddcad', default=True, description="Enable CAD interface based on Assimp")
    variant('ddg4', default=True, description="Enable the simulation part based on Geant4")
    variant('ddrec', default=True, description="Build DDRec subpackage.")
    variant('dddetectors', default=True, description="Build DDDetectors subpackage.")
    variant('ddcond', default=True, description="Build DDCond subpackage.")
    variant('ddalign', default=True, description="Build DDAlign subpackage.")
    variant('dddigi', default=True, description="Build DDDigi subpackage.")
    variant('ddeve', default=True, description="Build DDEve subpackage.")
    variant('utilityapps', default=True, description='Build UtilityApps subpackage.')

    # variants for other build options
    variant('xercesc', default=False, description="Enable 'Detector Builders' based on XercesC")
    variant('hepmc3', default=False, description="Enable build with hepmc3")
    variant('lcio', default=False, description="Enable build with lcio")
    variant('edm4hep', default=True, description="Enable build with edm4hep")
    variant('geant4units', default=False, description="Use geant4 units throughout")
    variant('tbb', default=False, description="Enable build with tbb")
    variant('debug', default=False,
            description="Enable debug build flag - adds extra info in"
            " some places in addtion to the debug build type")

    depends_on('cmake @3.12:', type='build')
    depends_on('ninja', type='build')
    depends_on('boost @1.49:')
    depends_on('boost +iostreams', when='+ddg4')
    depends_on('boost +system +filesystem', when='%gcc@:7')
    depends_on('root @6.08: +gdml +math +python')
    depends_on('root @6.08: +gdml +math +python +x +opengl', when="+ddeve")

    extends('python')
    depends_on('xerces-c', when='+xercesc')
    depends_on('geant4@10.2.2:', when='+ddg4')
    depends_on('assimp@5.0.2:', when='+ddcad')
    depends_on('hepmc3', when="+hepmc3")
    depends_on('intel-tbb', when='+tbb')
    depends_on('lcio', when="+lcio")
    depends_on('edm4hep', when="+edm4hep")
    depends_on('podio', when="+edm4hep")
    depends_on('py-pytest', type=('build', 'test'))

    # See https://github.com/AIDASoft/DD4hep/pull/771
    conflicts('^cmake@3.16:3.17.0', when='@1.15',
              msg='cmake version with buggy FindPython breaks dd4hep cmake config')
    conflicts('~ddrec+dddetectors', msg="Need to enable +ddrec to build +dddetectors.")

    def cmake_args(self):
        spec = self.spec
        cxxstd = spec['root'].variants['cxxstd'].value
        # root can be built with cxxstd=11, but dd4hep requires 14
        if cxxstd == "11":
            cxxstd = "14"
        args = [
            self.define_from_variant('DD4HEP_USE_EDM4HEP', 'edm4hep'),
            self.define_from_variant('DD4HEP_USE_XERCESC', 'xercesc'),
            self.define_from_variant('DD4HEP_USE_TBB', 'tbb'),
            self.define_from_variant('DD4HEP_USE_GEANT4', 'ddg4'),
            self.define_from_variant('DD4HEP_USE_LCIO', 'lcio'),
            self.define_from_variant('DD4HEP_USE_HEPMC3', 'hepmc3'),
            self.define_from_variant('DD4HEP_USE_GEANT4_UNITS', 'geant4units'),
            self.define_from_variant('DD4HEP_BUILD_DEBUG', 'debug'),
            # Downloads assimp from github and builds it on the fly.
            # However, with spack it is preferrable to have a proper external
            # dependency, so we disable it.
            self.define('DD4HEP_LOAD_ASSIMP', False),
            "-DCMAKE_CXX_STANDARD={0}".format(cxxstd),
            "-DBUILD_TESTING={0}".format(self.run_tests),
            "-DBOOST_ROOT={0}".format(spec['boost'].prefix),
            "-DBoost_NO_BOOST_CMAKE=ON",
            "-DPYTHON_EXECUTABLE={0}".format(spec['python'].command.path),
        ]
        subpackages = []
        if spec.satisfies('+ddg4'):
            subpackages += ['DDG4']
        if spec.satisfies('+ddcond'):
            subpackages += ['DDCond']
        if spec.satisfies('+ddcad'):
            subpackages += ['DDCAD']
        if spec.satisfies('+ddrec'):
            subpackages += ['DDRec']
        if spec.satisfies('+dddetectors'):
            subpackages += ['DDDetectors']
        if spec.satisfies('+ddalign'):
            subpackages += ['DDAlign']
        if spec.satisfies('+dddigi'):
            subpackages += ['DDDigi']
        if spec.satisfies('+ddeve'):
            subpackages += ['DDEve']
        if spec.satisfies('+utilityapps'):
            subpackages += ['UtilityApps']
        subpackages = ' '.join(subpackages)
        args += [self.define('DD4HEP_BUILD_PACKAGES', subpackages)]
        return args

    def setup_run_environment(self, env):
        # used p.ex. in ddsim to find DDDetectors dir
        env.set("DD4hepINSTALL", self.prefix)
        env.set("DD4HEP", self.prefix.examples)
        env.set("DD4hep_DIR", self.prefix)
        env.set("DD4hep_ROOT", self.prefix)

    def url_for_version(self, version):
        # dd4hep releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        base_url = self.url.rsplit('/', 1)[0]
        if len(version) == 1:
            major = version[0]
            minor, patch = 0, 0
        elif len(version) == 2:
            major, minor = version
            patch = 0
        else:
            major, minor, patch = version
        # By now the data is normalized enough to handle it easily depending
        # on the value of the patch version
        if patch == 0:
            version_str = 'v%02d-%02d.tar.gz' % (major, minor)
        else:
            version_str = 'v%02d-%02d-%02d.tar.gz' % (major, minor, patch)

        return base_url + '/' + version_str

    # dd4hep tests need to run after install step:
    # disable the usual check
    def check(self):
        pass

    # instead add custom check step that runs after installation
    @run_after('install')
    def build_test(self):
        with working_dir(self.build_directory):
            if self.run_tests:
                ninja('test')
