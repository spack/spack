# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os
import sys
from llnl.util.filesystem import fix_darwin_install_name


class Papi(AutotoolsPackage):
    """PAPI provides the tool designer and application engineer with a
       consistent interface and methodology for use of the performance
       counter hardware found in most major microprocessors. PAPI
       enables software engineers to see, in near real time, the
       relation between software performance and processor events.  In
       addition Component PAPI provides access to a collection of
       components that expose performance measurement opportunities
       across the hardware and software stack."""
    homepage = "http://icl.cs.utk.edu/papi/index.html"
    maintainers = ['G-Ragghianti']

    url = "http://icl.cs.utk.edu/projects/papi/downloads/papi-5.4.1.tar.gz"
    version('6.0.0.1', sha256='3cd7ed50c65b0d21d66e46d0ba34cd171178af4bbf9d94e693915c1aca1e287f')
    version('6.0.0', sha256='3442709dae3405c2845b304c06a8b15395ecf4f3899a89ceb4d715103cb4055f')
    version('5.7.0', sha256='d1a3bb848e292c805bc9f29e09c27870e2ff4cda6c2fba3b7da8b4bba6547589')
    version('5.6.0', sha256='49b7293f9ca2d74d6d80bd06b5c4be303663123267b4ac0884cbcae4c914dc47')
    version('5.5.1', sha256='49dc2c2323f6164c4a7e81b799ed690ee73158671205e71501f849391dd2c2d4')
    version('5.5.0', sha256='3ea15e6cc2354017335b659c1635409ddab1414e70573aa4df91fd892e99f98d')
    version('5.4.3', sha256='3aefd581e274f0a103f001f1ffd1009019b297c637e97f4b8c5fc13fa5a1e675')
    version('5.4.1', sha256='e131c1449786fe870322a949e44f974a5963824f683232e653fb570cc65d4e87')
    version('5.3.0', sha256='99f2f36398b370e75d100b4a189d5bc0ac4f5dd66df44d441f88fd32e1421524')

    variant('example', default=True, description='Install the example files')
    variant('infiniband', default=False, description='Enable Infiniband support')
    variant('powercap', default=False, description='Enable powercap interface support')
    variant('rapl', default=False, description='Enable RAPL support')
    variant('lmsensors', default=False, description='Enable lm_sensors support')
    variant('sde', default=False, description='Enable software defined events')

    depends_on('lm-sensors', when='+lmsensors')

    # Does not build with newer versions of gcc, see
    # https://bitbucket.org/icl/papi/issues/46/cannot-compile-on-arch-linux
    patch('https://bitbucket.org/icl/papi/commits/53de184a162b8a7edff48fed01a15980664e15b1/raw', sha256='64c57b3ad4026255238cc495df6abfacc41de391a0af497c27d0ac819444a1f8', when='@5.4.0:5.6.99%gcc@8:')

    configure_directory = 'src'

    def setup_build_environment(self, env):
        if '+lmsensors' in self.spec and self.version >= Version('6'):
            env.set('PAPI_LMSENSORS_ROOT', self.spec['lm-sensors'].prefix)

    def setup_run_environment(self, env):
        if '+lmsensors' in self.spec and self.version >= Version('6'):
            env.set('PAPI_LMSENSORS_ROOT', self.spec['lm-sensors'].prefix)

    def configure_args(self):
        options = ['MPICC=:']
        variants = filter(lambda x: self.spec.variants[x].value,
                          self.spec.variants)
        if variants:
            options.append('--with-components={0}'.format(' '.join(variants)))
        return options

    @run_before('configure')
    def component_configure(self):
        configure_script = Executable('./configure')
        if '+lmsensors' in self.spec and self.version < Version('6'):
            with working_dir("src/components/lmsensors"):
                configure_script(
                    "--with-sensors_incdir=%s/sensors" %
                    self.spec['lm-sensors'].headers.directories[0],
                    "--with-sensors_libdir=%s" %
                    self.spec['lm-sensors'].libs.directories[0])

    @run_before('build')
    def fix_build(self):
        # Don't use <malloc.h>
        for level in [".", "*", "*/*"]:
            files = glob.iglob(join_path(level, "*.[ch]"))
            filter_file(r"\<malloc\.h\>", "<stdlib.h>", *files)

    @run_after('build')
    def test(self):
        if self.run_tests:
            make("test")

    @run_after('install')
    def fix_darwin_install(self):
        # The shared library is not installed correctly on Darwin
        if sys.platform == 'darwin':
            os.rename(join_path(self.prefix.lib, 'libpapi.so'),
                      join_path(self.prefix.lib, 'libpapi.dylib'))
            fix_darwin_install_name(self.prefix.lib)
