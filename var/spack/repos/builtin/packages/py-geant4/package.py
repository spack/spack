# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGeant4(CMakePackage):
    """Python bindings for Geant4 (g4py)"""

    homepage = "http://geant4.cern.ch/"
    git = "https://gitlab.cern.ch/geant4/geant4.git"
    url = "https://gitlab.cern.ch/geant4/geant4/-/archive/v10.6.1/geant4-v10.6.1.tar.gz"

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    version('10.6.1', sha256='f6d883132f110eb036c69da2b21df51f13c585dc7b99d4211ddd32f4ccee1670')

    # take exact same Geant4 version
    for v in ['10.6.1']:
        depends_on('geant4@{0} +opengl+x11 cxxstd=11'.format(v),
                   when='@{0} cxxstd=11'.format(v),
                   type=['build', 'link', 'run'])
        depends_on('geant4@{0} +opengl+x11 cxxstd=14'.format(v),
                   when='@{0} cxxstd=14'.format(v),
                   type=['build', 'link', 'run'])
        depends_on('geant4@{0} +opengl+x11 cxxstd=17'.format(v),
                   when='@{0} cxxstd=17'.format(v),
                   type=['build', 'link', 'run'])

    depends_on('cmake@3.3:', type='build')

    # C++11/14/17 support
    depends_on('xerces-c cxxstd=11', when='cxxstd=11')
    depends_on('xerces-c cxxstd=14', when='cxxstd=14')
    depends_on('xerces-c cxxstd=17', when='cxxstd=17')

    depends_on('boost +python')
    extends('python')
    depends_on('root')

    root_cmakelists_dir = 'environments/g4py'

    def setup_build_environment(self, env):
        spec = self.spec
        env.set('GEANT4_INSTALL', spec['geant4'].prefix)
        # env.set('ROOTSYS', spec['root'].prefix)
        env.set('XERCESC_ROOT_DIR', spec['xerces-c'].prefix)
