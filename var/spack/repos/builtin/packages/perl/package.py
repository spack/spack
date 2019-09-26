# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Milton Woods <milton.woods@bom.gov.au>
# Date: March 22, 2017
# Author: George Hartzell <hartzell@alerce.com>
# Date: July 21, 2016
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#
import os
from contextlib import contextmanager

from llnl.util.lang import match_predicate

from spack import *


class Perl(Package):  # Perl doesn't use Autotools, it should subclass Package
    """Perl 5 is a highly capable, feature-rich programming language with over
       27 years of development."""

    homepage = "http://www.perl.org"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://www.cpan.org/src/5.0/perl-5.24.1.tar.gz"

    # see http://www.cpan.org/src/README.html for
    # explanation of version numbering scheme

    # Development releases (odd numbers)
    version('5.25.11', '37a398682c36cd85992b34b5c1c25dc1')

    # Maintenance releases (even numbers, recommended)
    version('5.28.0', sha256='7e929f64d4cb0e9d1159d4a59fc89394e27fa1f7004d0836ca0d514685406ea8')
    version('5.26.2', 'dc0fea097f3992a8cd53f8ac0810d523', preferred=True)
    version('5.24.1', '765ef511b5b87a164e2531403ee16b3c')

    # End of life releases
    version('5.22.4', '31a71821682e02378fcdadeed85688b8')
    version('5.22.3', 'aa4f236dc2fc6f88b871436b8d0fda95')
    version('5.22.2', '5767e2a10dd62a46d7b57f74a90d952b')
    version('5.22.1', '19295bbb775a3c36123161b9bf4892f1')
    version('5.22.0', 'e32cb6a8dda0084f2a43dac76318d68d')
    version('5.20.3', 'd647d0ea5a7a8194c34759ab9f2610cd')
    version('5.18.4', '1f9334ff730adc05acd3dd7130d295db')
    version('5.16.3', 'eb5c40f2575df6c155bc99e3fe0a9d82')

    extendable = True

    depends_on('gdbm')

    # there has been a long fixed issue with 5.22.0 with regard to the ccflags
    # definition.  It is well documented here:
    # https://rt.perl.org/Public/Bug/Display.html?id=126468
    patch('protect-quotes-in-ccflags.patch', when='@5.22.0')

    # Fix build on Fedora 28
    # https://bugzilla.redhat.com/show_bug.cgi?id=1536752
    patch('https://src.fedoraproject.org/rpms/perl/raw/004cea3a67df42e92ffdf4e9ac36d47a3c6a05a4/f/perl-5.26.1-guard_old_libcrypt_fix.patch', level=1, sha256='0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac', when='@:5.26.2')

    # Installing cpanm alongside the core makes it safe and simple for
    # people/projects to install their own sets of perl modules.  Not
    # having it in core increases the "energy of activation" for doing
    # things cleanly.
    variant('cpanm', default=True,
            description='Optionally install cpanm with the core packages.')

    variant('shared', default=True,
            description='Build a shared libperl.so library')

    variant('threads', default=True,
            description='Build perl with threads support')

    resource(
        name="cpanm",
        url="http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/App-cpanminus-1.7042.tar.gz",
        md5="e87f55fbcb3c13a4754500c18e89219f",
        destination="cpanm",
        placement="cpanm"
    )

    phases = ['configure', 'build', 'install']

    # On a lustre filesystem, patch may fail when files
    # aren't writeable so make pp.c user writeable
    # before patching. This should probably walk the
    # source and make everything writeable in the future.
    def do_stage(self, mirror_only=False):
        # Do Spack's regular stage
        super(Perl, self).do_stage(mirror_only)
        # Add write permissions on file to be patched
        filename = join_path(self.stage.source_path, 'pp.c')
        perm = os.stat(filename).st_mode
        os.chmod(filename, perm | 0o200)

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
        # https://github.com/spack/spack/pull/3081 and
        # https://github.com/spack/spack/pull/4416
        if spec.satisfies('%intel'):
            config_args.append('-Accflags={0}'.format(self.compiler.pic_flag))

        if '+shared' in spec:
            config_args.append('-Duseshrplib')

        if '+threads' in spec:
            config_args.append('-Dusethreads')

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
        if perl_bin_dirs:
            perl_bin_path = ':'.join(perl_bin_dirs)
            spack_env.prepend_path('PATH', perl_bin_path)
            run_env.prepend_path('PATH', perl_bin_path)
        if perl_lib_dirs:
            perl_lib_path = ':'.join(perl_lib_dirs)
            spack_env.prepend_path('PERL5LIB', perl_lib_path)
            run_env.prepend_path('PERL5LIB', perl_lib_path)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before perl modules' install() methods.
           In most cases, extensions will only need to have one line:
           perl('Makefile.PL','INSTALL_BASE=%s' % self.prefix)
        """

        # If system perl is used through packages.yaml
        # there cannot be extensions.
        if dependent_spec.package.is_extension:

            # perl extension builds can have a global perl
            # executable function
            module.perl = self.spec['perl'].command

            # Add variables for library directory
            module.perl_lib_dir = dependent_spec.prefix.lib.perl5

            # Make the site packages directory for extensions,
            # if it does not exist already.
            mkdirp(module.perl_lib_dir)

    @run_after('install')
    def filter_config_dot_pm(self):
        """Run after install so that Config.pm records the compiler that Spack
        built the package with.  If this isn't done, $Config{cc} will
        be set to Spack's cc wrapper script.  These files are read-only, which
        frustrates filter_file on some filesystems (NFSv4), so make them
        temporarily writable.
        """

        kwargs = {'ignore_absent': True, 'backup': False, 'string': False}

        # Find the actual path to the installed Config.pm file.
        perl = self.spec['perl'].command
        config_dot_pm = perl('-MModule::Loaded', '-MConfig', '-e',
                             'print is_loaded(Config)', output=str)

        with self.make_briefly_writable(config_dot_pm):
            match = 'cc *=>.*'
            substitute = "cc => '{cc}',".format(cc=self.compiler.cc)
            filter_file(match, substitute, config_dot_pm, **kwargs)

        # And the path Config_heavy.pl
        d = os.path.dirname(config_dot_pm)
        config_heavy = join_path(d, 'Config_heavy.pl')

        with self.make_briefly_writable(config_heavy):
            match = '^cc=.*'
            substitute = "cc='{cc}'".format(cc=self.compiler.cc)
            filter_file(match, substitute, config_heavy, **kwargs)

            match = '^ld=.*'
            substitute = "ld='{ld}'".format(ld=self.compiler.cc)
            filter_file(match, substitute, config_heavy, **kwargs)

            match = "^ccflags='"
            substitute = "ccflags='%s " % ' '\
                         .join(self.spec.compiler_flags['cflags'])
            filter_file(match, substitute, config_heavy, **kwargs)

    @contextmanager
    def make_briefly_writable(self, path):
        """Temporarily make a file writable, then reset"""
        perm = os.stat(path).st_mode
        os.chmod(path, perm | 0o200)
        yield
        os.chmod(path, perm)

    # ========================================================================
    # Handle specifics of activating and deactivating perl modules.
    # ========================================================================

    def perl_ignore(self, ext_pkg, args):
        """Add some ignore files to activate/deactivate args."""
        ignore_arg = args.get('ignore', lambda f: False)

        # Many perl packages describe themselves in a perllocal.pod file,
        # so the files conflict when multiple packages are activated.
        # We could merge the perllocal.pod files in activated packages,
        # but this is unnecessary for correct operation of perl.
        # For simplicity, we simply ignore all perllocal.pod files:
        patterns = [r'perllocal\.pod$']

        return match_predicate(ignore_arg, patterns)

    def activate(self, ext_pkg, view, **args):
        ignore = self.perl_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Perl, self).activate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        exts[ext_pkg.name] = ext_pkg.spec

    def deactivate(self, ext_pkg, view, **args):
        ignore = self.perl_ignore(ext_pkg, args)
        args.update(ignore=ignore)

        super(Perl, self).deactivate(ext_pkg, view, **args)

        extensions_layout = view.extensions_layout
        exts = extensions_layout.extension_map(self.spec)
        # Make deactivate idempotent
        if ext_pkg.name in exts:
            del exts[ext_pkg.name]
