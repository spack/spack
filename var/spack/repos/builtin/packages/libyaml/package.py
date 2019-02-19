# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libyaml(Package):
    """A C library for parsing and emitting YAML."""

    homepage = "https://github.com/yaml/libyaml"
    url      = "https://github.com/yaml/libyaml/archive/0.2.1.tar.gz"
    git      = "https://github.com/yaml/libyaml.git"

    version('master',     branch='master')
    version('0.2.1',      sha256='1d2aeb87f7d317f1496e4c39410d913840714874a354970300f375eec9303dc4')
    version('0.1.7',      sha256='e1884d0fa1eec8cf869ac6bebbf25391e81956aa2970267f974a9fa5e0b968e2')
    version('0.1.6',      sha256='a0ad4b8cfa4b26c669c178af08147449ea7e6d50374cc26503edc56f3be894cf')
    version('0.1.5',      sha256='79511ce3c1195e3c83157b7243bc98c48f945662ed75d8606aea9182eb8dccd5')
    version('0.1.4',      sha256='6406d298a7889ad8e107239d3154c3540dbc0820ff4c5e889c60019fc2bf672b')
    version('0.1.3',      sha256='87bd8237880ccf3f993cfa5718c1081673813d11572ca469b24cfc3df5a425f5')
    version('0.1.2',      sha256='fa395384d1964ea2039744087fa825ed3ac321222df17ad66f198fecc48e39cd')
    version('0.1.1',      sha256='1183790fc59795a77bf4c8193aa24439dc0f8712ac37e4639be2e821c9d4e463')

    depends_on('automake')
    depends_on('autoconf')
    depends_on('libtool')

    phases = ['bootstrap', 'install']

    def bootstrap(self, spec, prefix):
        bootstrap = Executable('./bootstrap')
        bootstrap()

    def install(self, spec, prefix):
        configure('--disable-dependency-tracking',
                  '--prefix=%s' % self.spec.prefix)
        make('install')
