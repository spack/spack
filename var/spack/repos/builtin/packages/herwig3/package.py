# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *
from spack.pkg.builtin.boost import Boost


class Herwig3(AutotoolsPackage):
    """Herwig is a multi-purpose particle physics event generator."""

    homepage = "https://herwig.hepforge.org"
    url      = "https://herwig.hepforge.org/downloads/Herwig-7.2.1.tar.bz2"

    tags = ['hep']

    version('7.2.1', sha256='d4fff32f21c5c08a4b2e563c476b079859c2c8e3b78d853a8a60da96d5eea686')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('lhapdf')
    depends_on('lhapdfsets')
    depends_on('thepeg@2.2.1', when='@7.2.1')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('python', type=('build', 'run'))
    depends_on('gsl')
    depends_on('fastjet')
    depends_on('vbfnlo@3:')
    depends_on('madgraph5amc')
    depends_on('njet')
    depends_on('py-gosam', when='^python@2.7.0:2.7')
    depends_on('gosam-contrib')
    depends_on('openloops')

    force_autoreconf = True

    def autoreconf(self, spec, prefix):
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = ['--with-gsl=' + self.spec['gsl'].prefix,
                '--with-thepeg=' + self.spec['thepeg'].prefix,
                '--with-thepeg-headers=' + self.spec['thepeg'].prefix.include,
                '--with-fastjet=' + self.spec['fastjet'].prefix,
                '--with-boost=' + self.spec['boost'].prefix,
                '--with-madgraph=' + self.spec['madgraph5amc'].prefix,
                '--with-openloops=' + self.spec['openloops'].prefix,
                '--with-gosam-contrib=' + self.spec['gosam-contrib'].prefix,
                '--with-njet=' + self.spec['njet'].prefix,
                '--with-vbfnlo=' + self.spec['vbfnlo'].prefix]

        if self.spec.satisfies('^python@2.7.0:2.7'):
            args.append('--with-gosam=' + self.spec['gosam'].prefix)

        return args

    def flag_handler(self, name, flags):
        if name == 'fflags':
            flags.append('-std=legacy')
            return (flags, None, None)
        return (flags, None, None)

    def setup_build_environment(self, env):
        thepeg_home = self.spec['thepeg'].prefix
        env.prepend_path('LD_LIBRARY_PATH', thepeg_home.lib.ThePEG)
        env.set('HERWIGINCLUDE', '-I' + self.prefix.include)
        env.set('BOOSTINCLUDE', '-I' + self.spec['boost'].prefix.include)
        env.set('HERWIGINSTALL', self.prefix)

    def build(self, spec, prefix):
        make()
        with working_dir('MatrixElement/FxFx'):
            make()

    def install(self, spec, prefix):
        make('install')
        with working_dir('MatrixElement/FxFx'):
            make('install')
