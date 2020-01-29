# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gaudi(CMakePackage):
    """An experiment-independent HEP event data processing framework"""

    homepage = "http://gaudi.web.cern.ch/gaudi/"
    git      = "https://gitlab.cern.ch/gaudi/Gaudi.git"

    version('develop', branch='master')
    version('30.5',    commit='2c70e73ee5b543b26197b90dd59ea4e4d359d230')
    version('31.0',    commit='aeb156f0c40571b5753a9e1dab31e331491b2f3e')

    variant('tests', default=False,
            description='Prepare to run the test suite')
    variant('optional', default=False,
            description='Build most optional components')
    variant('vtune', default=False,
            description='Build with Intel VTune profiler support')

    # These dependencies are needed for a minimal Gaudi build
    depends_on('boost@1.67.0: +python')
    depends_on('cmake', type='build')
    depends_on('intel-tbb')
    depends_on('libuuid')
    depends_on('python@:2.99.99')
    depends_on('py-xenv@develop_2018-12-20:')
    depends_on('range-v3')
    depends_on('root +python +root7 +ssl +tbb +threads')
    depends_on('zlib')

    # These dependencies are required by the Gaudi test suite
    depends_on('aida', when='+tests')
    depends_on('clhep', when='+tests')
    depends_on('cppunit', when='+tests')
    depends_on('gdb', when='+tests')
    depends_on('gperftools', when='+tests')
    depends_on('heppdt@:2.99.99', when='+tests')
    depends_on('py-networkx', when='+tests')
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
