#
# Author: George Hartzell <hartzell@alerce.com>
# Date: July 21, 2016
# Author: Justin Too <justin@doubleotoo.com>
# Date: September 6, 2015
#
from spack import *


class Perl(Package):
    """Perl 5 is a highly capable, feature-rich programming language with over
       27 years of development."""
    homepage = "http://www.perl.org"
    url      = "http://www.cpan.org/src/5.0/perl-5.22.2.tar.gz"

    version('5.24.0', 'c5bf7f3285439a2d3b6a488e14503701')
    version('5.22.2', '5767e2a10dd62a46d7b57f74a90d952b')
    version('5.20.3', 'd647d0ea5a7a8194c34759ab9f2610cd')
    # 5.18.4 fails with gcc-5
    # https://rt.perl.org/Public/Bug/Display.html?id=123784
    # version('5.18.4' , '1f9334ff730adc05acd3dd7130d295db')

    # Installing cpanm alongside the core makes it safe and simple for
    # people/projects to install their own sets of perl modules.  Not
    # having it in core increases the "energy of activation" for doing
    # things cleanly.
    variant('cpanm', default=True,
            description='Having cpanm in core simplifies adding modules.')
    variant('cpanm_version', default='1.7042',
            description='Version of cpanm to install into core if +cpanm.')

    def install(self, spec, prefix):
        configure = Executable('./Configure')
        configure("-des", "-Dprefix=" + prefix)
        make()
        if self.run_tests:
            make("test")
        make("install")

        if '+cpanm' in spec:
            perl_exe = join_path(prefix.bin, 'perl')
            perl = Executable(perl_exe)
            cpanm_installer = join_path(self.package_dir, 'cpanm-installer.pl')
            cpanm_version = spec.variants['cpanm_version'].value
            cpanm_package_spec = 'App::cpanminus' + '@' + cpanm_version
            perl(cpanm_installer, cpanm_package_spec)
