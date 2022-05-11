# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Racket(Package):
    """The Racket programming language."""

    homepage = "https://www.racket-lang.org"

    maintainers = ['arjunguha', 'elfprince13']

    version('8.3', '3b963cd29ae119e1acc2c6dc4781bd9f25027979589caaae3fdfc021aac2324b')

    depends_on('libffi', type=('build', 'link', 'run'))
    depends_on('patchutils')
    depends_on('libtool', type=('build'))

    phases = ['configure', 'build', 'install']

    def url_for_version(self, version):
        return "https://mirror.racket-lang.org/installers/{0}/racket-minimal-{0}-src-builtpkgs.tgz".format(version)

    variant('cs', default=True, description='Build Racket CS (new ChezScheme VM)')
    variant('bc', default=False, description='Build Racket BC (old MZScheme VM)')
    variant('shared', default=True, description="Enable shared")
    variant('jit', default=True, description="Just-in-Time Compilation")

    parallel = False
    extendable = True

    def toggle(self, spec, variant):
        toggle_text = ("enable" if spec.variants[variant].value else "disable")
        return "--{0}-{1}".format(toggle_text, variant)

    def configure(self, spec, prefix):
        with working_dir('src'):
            configure = Executable("./configure")
            configure_args = [self.toggle(spec, 'cs'),
                              self.toggle(spec, 'bc'),
                              self.toggle(spec, 'jit')]
            toggle_shared = self.toggle(spec, 'shared')
            if sys.platform == 'darwin':
                configure_args += ["--enable-macprefix"]
                if "+xonx" in spec:
                    configure_args += ["--enable-xonx", toggle_shared]
            else:
                configure_args += [toggle_shared]
            configure_args += ["--prefix={0}".format(prefix)]
            configure(*configure_args)

    def build(self, spec, prefix):
        with working_dir('src'):
            if spec.variants["bc"].value:
                make("bc")
            if spec.variants["cs"].value:
                make("cs")

    def install(self, spec, prefix):
        with working_dir('src'):
            if spec.variants["bc"].value:
                make('install-bc')
            if spec.variants["cs"].value:
                make('install-cs')
