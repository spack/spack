# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class Sherpa(AutotoolsPackage):
    """Sherpa is a Monte Carlo event generator for the Simulation of
    High-Energy Reactions of PArticles in lepton-lepton, lepton-photon,
    photon-photon, lepton-hadron and hadron-hadron collisions."""

    homepage = "https://sherpa-team.gitlab.io"
    url      = "https://gitlab.com/sherpa-team/sherpa/-/archive/v2.2.11/sherpa-v2.2.11.tar.gz"
    list_url = "https://gitlab.com/sherpa-team/sherpa/-/tags"
    git      = "https://gitlab.com/sherpa-team/sherpa.git"

    tags = ['hep', 'eic']

    maintainers = ['wdconinc', 'vvolkl']
    version('2.2.12', sha256='4ba78098e45aaac0bc303d1b5abdc15809f30b407abf9457d99b55e63384c83d')
    version('2.2.11', sha256='5e12761988b41429f1d104f84fdf352775d233cde7a165eb64e14dcc20c3e1bd')
    version('2.2.10', sha256='ae23bc8fdcc9f8c26becc41692822233b62203cd72a7e0dab2ca19316aa0aad7', deprecated=True)
    version('2.2.9', sha256='ebc836d42269a0c4049d3fc439a983d19d12595d9a06db2d18765bd1e301923e', deprecated=True)
    version('2.2.8', sha256='ff198cbae5de445e6fe383151021ef24b1628dffc0da6bf3737753f6672a0091', deprecated=True)
    version('2.0.0', sha256='0e873b27bb1be46ca5ed451d1b8514ca84c10221057b11be5952180076e6f848', deprecated=True)
    version('1.3.1', sha256='31881207838d341358db64e3fdadfeee1ea2f6d1cb42f370014f622f579159ae', deprecated=True)
    version('1.3.0', sha256='08b13c65b66f2edde6996d2a06762a12a0682ffb64bca43654df47321e5039a0', deprecated=True)
    version('1.2.3', sha256='029727337a430d6675a1a12dce3ced0411041e79ddaf4ce3b9466035cf6c8804', deprecated=True)
    version('1.2.2', sha256='6e7b5ea80b99f1378519009e494030d6cf4c4491f91218d749eabb8ffaad9ac1', deprecated=True)
    version('1.2.1', sha256='838462f4a1e8768135363aa6b8532fd8f5e5789a269b858f8e3728ab37f6a1d1', deprecated=True)
    version('1.2.0', sha256='509508fd0ad72aaf55ab484da8b6bc0b31688c955adcda62a3e8f94689cebf99', deprecated=True)
    version('1.1.3', sha256='6335e5eb1fc304e9618496d3ddb198b3591e57b27db6e876af8fd649a8b98c93', deprecated=True)
    version('1.1.2', sha256='e1689cad6700dc013af0afb0d33729ac2b5e9841d2f325c85b10d773e7f8a80e', deprecated=True)
    version('1.1.1', sha256='b80e1d75934be79b73400d2c95d96e88651626ea29ddcb9d8fde9c1812039e29', deprecated=True)
    version('1.1.0', sha256='8052d137d668353dc710f8691b921e772820d39e20361f0d616ee2da1ac798f2', deprecated=True)
    version('1.0.9', sha256='fe28db91ea8264364395c7e5efeeae3e5c01ea1343e0db7fe13924c6f17fb963', deprecated=True)
    version('1.0.8', sha256='6e346bafd13b5b05ad566a73759da6d5e64d65c5036780cc4911d93277e891fa', deprecated=True)
    version('1.0.7', sha256='d1eeefd96c6822ea8eb926447ca91ec4a1c714e4746323e92b1e17764e51ff0b', deprecated=True)
    version('1.0.6', sha256='358d417ec3afde24618c222bc9b742bc5102d435622b3cd6f2e3f72d03656255', deprecated=True)

    _cxxstd_values = ('11', '14', '17')
    variant('cxxstd',    default='11', values=_cxxstd_values, multi=False,
            description='Use the specified C++ standard when building')

    variant('analysis',   default=True, description='Enable analysis components')
    variant('mpi',        default=False, description='Enable MPI')
    variant('python',     default=False, description='Enable Python API')
    variant('hepmc2',     default=True, description='Enable HepMC (version 2.x) support')
    variant('hepmc3',     default=True, description='Enable HepMC (version 3.x) support')
    variant('hepmc3root', default=False, description='Enable HepMC (version 3.1+) ROOT support')
    variant('rivet',      default=False, description='Enable Rivet support')
    variant('fastjet',    default=True, description='Enable FASTJET')
    variant('openloops',  default=False, description='Enable OpenLoops')
    variant('recola',     default=False, description='Enable Recola')
    variant('lhole',      default=False, description='Enable Les Houches One-Loop Generator interface')
    variant('root',       default=False, description='Enable ROOT support')
    variant('lhapdf',     default=True, description='Enable LHAPDF support')
    variant('gzip',       default=False, description='Enable gzip support')
    variant('pythia',     default=True, description='Enable fragmentation/decay interface to Pythia')
    variant('blackhat',   default=False, description='Enable BLACKHAT support')
    variant('ufo',        default=False, description='Enable UFO support')
    # hztool and cernlib not yet in spack
    # variant('hztool',     default=False, description='Enable HZTOOL support')
    # variant('cernlib',    default=False, description='Enable CERNLIB support')

    variant('cms',        default=False, description="Append CXXFLAGS used by CMS experiment")

    # Note that the delphes integration seems utterly broken: https://sherpa.hepforge.org/trac/ticket/305

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('texinfo',  type='build')
    depends_on('sqlite')

    depends_on('mpi',       when='+mpi')
    depends_on('python',    when='+python')
    depends_on('swig',      when='+python', type='build')
    depends_on('hepmc',     when='+hepmc2')
    depends_on('hepmc3',    when='+hepmc3')
    depends_on('hepmc3 +rootio', when='+hepmc3root')
    depends_on('rivet',     when='+rivet')
    depends_on('fastjet',   when='+fastjet')
    depends_on('openloops', when='+openloops')
    depends_on('recola',    when='+recola')
    depends_on('root',      when='+root')
    depends_on('lhapdf',    when='+lhapdf')
    depends_on('gzip',      when='+gzip')
    depends_on('pythia6',   when='+pythia')
    depends_on('blackhat',  when='+blackhat')
    # depends_on('cernlib',   when='+cernlib')

    for std in _cxxstd_values:
        depends_on('root cxxstd=' + std, when='+root cxxstd=' + std)

    def patch(self):
        filter_file(r'#include <sys/sysctl.h>',
                    '#ifdef ARCH_DARWIN\n#include <sys/sysctl.h>\n#endif',
                    'ATOOLS/Org/Run_Parameter.C')

    def configure_args(self):
        args = []
        args.append('--enable-shared')
        args.append('--enable-binreloc')
        args.append('--enable-static')
        args.append('--enable-hepevtsize=200000')
        args.append('--with-sqlite3=' + self.spec['sqlite'].prefix)
        args.extend(self.enable_or_disable('mpi'))
        args.extend(self.enable_or_disable('pyext', variant='python'))
        args.extend(self.enable_or_disable('analysis'))
        args.extend(self.enable_or_disable('lhole'))
        args.extend(self.enable_or_disable('gzip'))
        args.extend(self.enable_or_disable('pythia'))
        hepmc_root = lambda x: self.spec['hepmc'].prefix
        args.extend(self.enable_or_disable('hepmc2', activation_value=hepmc_root))
        args.extend(self.enable_or_disable('hepmc3', activation_value='prefix'))
        args.extend(self.enable_or_disable('rivet', activation_value='prefix'))
        args.extend(self.enable_or_disable('fastjet', activation_value='prefix'))
        args.extend(self.enable_or_disable('openloops', activation_value='prefix'))
        args.extend(self.enable_or_disable('recola', activation_value='prefix'))
        args.extend(self.enable_or_disable('root', activation_value='prefix'))
        args.extend(self.enable_or_disable('lhapdf', activation_value='prefix'))
        # args.extend(self.enable_or_disable('hztool', activation_value='prefix'))
        # args.extend(self.enable_or_disable('cernlib', activation_value='prefix'))
        args.extend(self.enable_or_disable('blackhat', activation_value='prefix'))
        args.extend(self.enable_or_disable('ufo'))

        if self.spec.satisfies('+mpi'):
            args.append('CC=' + self.spec['mpi'].mpicc)
            args.append('MPICXX=' + self.spec['mpi'].mpicxx)
            args.append('CXX=' + self.spec['mpi'].mpicxx)
            args.append('FC=' + self.spec['mpi'].mpifc)

        if self.spec.satisfies('+cms'):
            if platform.machine() == 'x86_64':
                args.append('CXXFLAGS=-fuse-cxa-atexit -m64 -O2 -std=c++0x')
            else:
                args.append('CXXFLAGS=-fuse-cxa-atexit -O2 -std=c++0x')

        return args
