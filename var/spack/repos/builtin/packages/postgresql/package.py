# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Postgresql(AutotoolsPackage):
    """PostgreSQL is a powerful, open source object-relational database system.
    It has more than 15 years of active development and a proven architecture
    that has earned it a strong reputation for reliability, data integrity, and
    correctness."""

    homepage = "http://www.postgresql.org/"
    url      = "http://ftp.postgresql.org/pub/source/v9.3.4/postgresql-9.3.4.tar.bz2"
    list_url = "http://ftp.postgresql.org/pub/source"
    list_depth = 1

    version('11.2',   sha256='2676b9ce09c21978032070b6794696e0aa5a476e3d21d60afc036dc0a9c09405')
    version('11.1',   sha256='90815e812874831e9a4bf6e1136bf73bc2c5a0464ef142e2dfea40cda206db08')
    version('11.0',   sha256='bf9bba03d0c3902c188af12e454b35343c4a9bf9e377ec2fe50132efb44ef36b')
    version('10.7',   sha256='bfed1065380c1bba927bfe51f23168471373f26e3324cbad859269cc32733ede')
    version('10.6',   sha256='68a8276f08bda8fbefe562faaf8831cb20664a7a1d3ffdbbcc5b83e08637624b')
    version('10.5',   sha256='6c8e616c91a45142b85c0aeb1f29ebba4a361309e86469e0fb4617b6a73c4011')
    version('10.4',   sha256='1b60812310bd5756c62d93a9f93de8c28ea63b0df254f428cd1cf1a4d9020048')
    version('10.3', '506498796a314c549388cafb3d5c717a')
    version('10.2', 'e97c3cc72bdf661441f29069299b260a')
    version('10.1',   sha256='3ccb4e25fe7a7ea6308dea103cac202963e6b746697366d72ec2900449a5e713')
    version('10.0',   sha256='712f5592e27b81c5b454df96b258c14d94b6b03836831e015c65d6deeae57fd1')
    version('9.6.12', sha256='2e8c8446ba94767bda8a26cf5a2152bf0ae68a86aaebf894132a763084579d84')
    version('9.6.11', sha256='38250adc69a1e8613fb926c894cda1d01031391a03648894b9a6e13ff354a530')
    version('9.5.3', '3f0c388566c688c82b01a0edf1e6b7a0')
    version('9.3.4', 'd0a41f54c377b2d2fab4a003b0dac762')

    variant('client_only', default=False,
            description='Build and install client only.')
    variant('threadsafe', default=False, description='Build with thread safe.')
    variant('lineedit', default='readline',
            values=('readline', 'libedit', 'none'), multi=False,
            description='Line editing library')
    variant('python', default=False, description='Enable Python bindings.')
    variant('perl', default=False, description='Enable Perl bindings.')
    variant('tcl', default=False, description='Enable Tcl bindings.')
    variant('gssapi', default=False,
            description='Build with GSSAPI functionality.')

    depends_on('readline', when='lineedit=readline')
    depends_on('libedit', when='lineedit=libedit')
    depends_on('openssl')
    depends_on('tcl', when='+tcl')
    depends_on('perl', when='+perl')
    depends_on('python', when='+python')

    def configure_args(self):
        config_args = ["--with-openssl"]

        if '+threadsafe' in self.spec:
            config_args.append('--enable-thread-safety')
        else:
            config_args.append('--disable-thread-safety')

        if self.spec.variants['lineedit'].value == 'libedit':
            config_args.append('--with-libedit-preferred')
        elif self.spec.variants['lineedit'].value == 'none':
            config_args.append('--without-readline')

        if '+gssapi' in self.spec:
            config_args.append('--with-gssapi')

        if '+python' in self.spec:
            config_args.append('--with-python')

        if '+perl' in self.spec:
            config_args.append('--with-perl')

        if '+tcl' in self.spec:
            config_args.append('--with-tcl')

        return config_args

    def install(self, spec, prefix):
        if '+client-only' in self.spec:
            for subdir in ('bin', 'include', 'interfaces', 'pl'):
                with working_dir(os.path.join('src', subdir)):
                    make('install')
        else:
            AutotoolsPackage.install(self, spec, prefix)

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        if '+perl' in spec:
            run_env.prepend_path('PERL5LIB', self.prefix.lib)
        if '+tcl' in spec:
            run_env.prepend_path('TCLLIBPATH', self.prefix.lib)
        if '+python' in spec:
            run_env.prepend_path('PYTHONPATH', self.prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spec = self.spec

        if '+perl' in spec:
            spack_env.prepend_path('PERL5LIB', self.prefix.lib)
            run_env.prepend_path('PERL5LIB', self.prefix.lib)
        if '+tcl' in spec:
            spack_env.prepend_path('TCLLIBPATH', self.prefix.lib)
            run_env.prepend_path('TCLLIBPATH', self.prefix.lib)
        if '+python' in spec:
            spack_env.prepend_path('PYTHONPATH', self.prefix.lib)
            run_env.prepend_path('PYTHONPATH', self.prefix.lib)
