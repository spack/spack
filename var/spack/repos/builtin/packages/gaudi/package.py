# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gaudi(CMakePackage):
    """An experiment-independent HEP event data processing framework"""

    homepage = "http://gaudi.web.cern.ch/gaudi/"
    git      = "https://gitlab.cern.ch/gaudi/Gaudi.git"
    url      = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v33r1/Gaudi-v33r1.tar.gz"

    version('master', branch='master')
    # major cmake config overhaul already in use by some
    version('develop', git='https://gitlab.cern.ch/clemenci/Gaudi.git', branch='cmake-modernisation')
    version('33.1', sha256='7eb6b2af64aeb965228d4b6ea66c7f9f57f832f93d5b8ad55c9105235af5b042')
    version('33.0', sha256='76a967c41f579acc432593d498875dd4dc1f8afd5061e692741a355a9cf233c8')
    version('32.2', sha256='e9ef3eb57fd9ac7b9d5647e278a84b2e6263f29f0b14dbe1321667d44d969d2e')

    maintainers = ['drbenmorgan', "vvolkl"]

    variant('tests', default=False,
            description='Prepare to run the test suite')
    variant('optional', default=False,
            description='Build most optional components')
    variant('vtune', default=False,
            description='Build with Intel VTune profiler support')

    # only build subdirectory GaudiExamples when +tests
    patch("build_testing.patch", when="@:33.1")
    # fix for the new cmake config, should be merged in branch
    patch('python2.patch', when="@develop")
    # fixes for the cmake config which could not find newer boost versions
    patch("link_target_fixes.patch", when="@33.0:33.1")
    patch("link_target_fixes32.patch", when="@:32.2")

    # These dependencies are needed for a minimal Gaudi build
    depends_on('boost@1.67.0: +python')
    depends_on('cmake', type='build')
    depends_on('cppgsl')
    depends_on('intel-tbb')
    depends_on('libuuid')
    # some bugs with python 3.8
    depends_on('python@:3.7.99')
    depends_on('py-setuptools@:45.99.99', when='^python@:2.7.99')
    depends_on('py-six')
    depends_on('py-xenv@develop_2018-12-20:')
    depends_on('range-v3')
    depends_on('root +python +root7 +ssl +tbb +threads')
    depends_on('zlib')

    depends_on('py-nose', when="@develop")

    # These dependencies are required by the Gaudi test suite
    depends_on('aida', when='+tests')
    depends_on('clhep', when='+tests')
    depends_on('cppunit', when='+tests')
    depends_on('gdb', when='+tests')
    depends_on('gperftools', when='+tests')
    depends_on('heppdt@:2.99.99', when='+tests')
    depends_on('py-networkx@:2.2', when='+tests ^python@:2.7.99')
    depends_on('py-networkx', when='+tests ^python@3.0.0:')
    depends_on('py-nose', when='+tests')
    depends_on('py-setuptools', when='+tests')
    depends_on('relax', when='+tests')
    depends_on('xerces-c', when='+tests')

    # Adding these dependencies triggers the build of most optional components
    depends_on('aida', when='+optional')
    depends_on('clhep', when='+optional')
    depends_on('cppgsl', when='+optional')
    depends_on('cppunit', when='+optional')
    depends_on('doxygen +graphviz', when='+optional')
    depends_on('gperftools', when='+optional')
    depends_on('gsl', when='+optional')
    depends_on('heppdt@:2.99.99', when='+optional')
    depends_on('jemalloc', when='+optional')
    depends_on('libpng', when='+optional')
    depends_on('libunwind', when='+optional')
    depends_on('relax', when='+optional')
    depends_on('xerces-c', when='+optional')
    # NOTE: pocl cannot be added as a minimal OpenCL implementation because
    #       ROOT does not like being exposed to LLVM symbols.

    # The Intel VTune dependency is taken aside because it requires a license
    depends_on('intel-parallel-studio -mpi +vtune', when='+vtune')

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define_from_variant("GAUDI_USE_AIDA", "optional"),
            self.define_from_variant("GAUDI_USE_XERCESC", "optional"),
            self.define_from_variant("GAUDI_USE_CLHEP", "optional"),
            self.define_from_variant("GAUDI_USE_HEPPDT", "optional"),
            self.define_from_variant("GAUDI_USE_CPPUNIT", "optional"),
            self.define_from_variant("GAUDI_USE_UNWIND", "optional"),
            self.define_from_variant("GAUDI_USE_GPERFTOOLS", "optional"),
            self.define_from_variant("GAUDI_USE_DOXYGEN", "optional"),
            self.define_from_variant("GAUDI_USE_INTELAMPLIFIER", "optional"),
            self.define_from_variant("GAUDI_USE_JEMALLOC", "optional"),
            # this is not really used in spack builds, but needs to be set
            "-DHOST_BINARY_TAG=x86_64-linux-gcc9-opt",
        ]
        return args

    def url_for_version(self, version):
        major = str(version[0])
        minor = str(version[1])
        url = "https://gitlab.cern.ch/gaudi/Gaudi/-/archive/v{0}r{1}/Gaudi-v{0}r{1}.tar.gz".format(major, minor)
        return url
