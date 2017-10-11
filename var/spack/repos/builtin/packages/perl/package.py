##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
# Author: Milton Woods <milton.woods@bom.gov.au>
# Date: March 22, 2017
# Author: George Hartzell <hartzell@alerce.com>
# Date: July 21, 2016
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#
from spack import *
import os


class Perl(Package):  # Perl doesn't use Autotools, it should subclass Package
    """Perl 5 is a highly capable, feature-rich programming language with over
       27 years of development."""

    homepage = "http://www.perl.org"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://www.cpan.org/src/5.0/perl-5.24.1.tar.gz"

    # Development releases
    version('5.25.11', '37a398682c36cd85992b34b5c1c25dc1')

    # Maintenance releases (recommended)
    version('5.24.1', '765ef511b5b87a164e2531403ee16b3c', preferred=True)
    version('5.22.3', 'aa4f236dc2fc6f88b871436b8d0fda95')

    # Misc releases that people need
    version('5.22.2', '5767e2a10dd62a46d7b57f74a90d952b')
    version('5.22.1', '19295bbb775a3c36123161b9bf4892f1')

    # End of life releases
    version('5.20.3', 'd647d0ea5a7a8194c34759ab9f2610cd')
    version('5.18.4', '1f9334ff730adc05acd3dd7130d295db')
    version('5.16.3', 'eb5c40f2575df6c155bc99e3fe0a9d82')

    extendable = True

    depends_on('gdbm')

    # Installing cpanm alongside the core makes it safe and simple for
    # people/projects to install their own sets of perl modules.  Not
    # having it in core increases the "energy of activation" for doing
    # things cleanly.
    variant('cpanm', default=True,
            description='Optionally install cpanm with the core packages.')

    variant('shared', default=True,
            description='Build a shared libperl.so library')

    resource(
        name="cpanm",
        url="http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.7042.tar.gz",
        md5="e87f55fbcb3c13a4754500c18e89219f",
        destination="cpanm",
        placement="cpanm"
    )

    phases = ['configure', 'build', 'install']

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        config_args = [
            '-des',
            '-Dprefix={0}'.format(prefix),
            '-Dlocincpth=' + self.spec['gdbm'].prefix.include,
            '-Dloclibpth=' + self.spec['gdbm'].prefix.lib,
        ]

        # Extensions are installed into their private tree via
        # `INSTALL_BASE`/`--install_base` (see [1]) which results in a
        # "predictable" installation tree that sadly does not match the
        # Perl core's @INC structure.  This means that when activation
        # merges the extension into the extendee[2], the directory tree
        # containing the extensions is not on @INC and the extensions can
        # not be found.
        #
        # This bit prepends @INC with the directory that is used when
        # extensions are activated [3].
        #
        # [1] https://metacpan.org/pod/ExtUtils::MakeMaker#INSTALL_BASE
        # [2] via the activate method in the PackageBase class
        # [3] https://metacpan.org/pod/distribution/perl/INSTALL#APPLLIB_EXP
        config_args.append('-Accflags=-DAPPLLIB_EXP=\\"' +
                           self.prefix.lib.perl5 + '\\"')

        # Discussion of -fPIC for Intel at:
        # https://github.com/LLNL/spack/pull/3081 and
        # https://github.com/LLNL/spack/pull/4416
        if spec.satisfies('%intel'):
            config_args.append('-Accflags={0}'.format(self.compiler.pic_flag))

        if '+shared' in spec:
            config_args.append('-Duseshrplib')

        return config_args

    def configure(self, spec, prefix):
        configure = Executable('./Configure')
        configure(*self.configure_args())

    def build(self, spec, prefix):
        make()

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def test(self):
        make('test')

    def install(self, spec, prefix):
        make('install')

    @run_after('install')
    def install_cpanm(self):
        spec = self.spec

        if '+cpanm' in spec:
            with working_dir(join_path('cpanm', 'cpanm')):
                perl = spec['perl'].command
                perl('Makefile.PL')
                make()
                make('install')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set PATH and PERL5LIB to include the extension and
           any other perl extensions it depends on,
           assuming they were installed with INSTALL_BASE defined."""
        perl_lib_dirs = []
        perl_bin_dirs = []
        for d in dependent_spec.traverse(
                deptype=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                perl_lib_dirs.append(d.prefix.lib.perl5)
                perl_bin_dirs.append(d.prefix.bin)
        perl_bin_path = ':'.join(perl_bin_dirs)
        perl_lib_path = ':'.join(perl_lib_dirs)
        spack_env.prepend_path('PATH', perl_bin_path)
        spack_env.prepend_path('PERL5LIB', perl_lib_path)
        run_env.prepend_path('PATH', perl_bin_path)
        run_env.prepend_path('PERL5LIB', perl_lib_path)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before perl modules' install() methods.
           In most cases, extensions will only need to have one line:
           perl('Makefile.PL','INSTALL_BASE=%s' % self.prefix)
        """

        # perl extension builds can have a global perl executable function
        module.perl = self.spec['perl'].command

        # Add variables for library directory
        module.perl_lib_dir = dependent_spec.prefix.lib.perl5

        # Make the site packages directory for extensions,
        # if it does not exist already.
        if dependent_spec.package.is_extension:
            mkdirp(module.perl_lib_dir)

    @run_after('install')
    def filter_config_dot_pm(self):
        """Run after install so that Config.pm records the compiler that Spack
        built the package with.  If this isn't done, $Config{cc} will
        be set to Spack's cc wrapper script.
        """

        kwargs = {'ignore_absent': True, 'backup': False, 'string': False}

        # Find the actual path to the installed Config.pm file.
        perl = self.spec['perl'].command
        config_dot_pm = perl('-MModule::Loaded', '-MConfig', '-e',
                             'print is_loaded(Config)', output=str)

        match = 'cc *=>.*'
        substitute = "cc => '{cc}',".format(cc=self.compiler.cc)
        filter_file(match, substitute, config_dot_pm, **kwargs)

        # And the path Config_heavy.pl
        d = os.path.dirname(config_dot_pm)
        config_heavy = join_path(d, 'Config_heavy.pl')

        match = '^cc=.*'
        substitute = "cc='{cc}'".format(cc=self.compiler.cc)
        filter_file(match, substitute, config_heavy, **kwargs)

        match = '^ld=.*'
        substitute = "ld='{ld}'".format(ld=self.compiler.cc)
        filter_file(match, substitute, config_heavy, **kwargs)
