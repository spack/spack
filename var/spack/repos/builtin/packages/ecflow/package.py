# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Ecflow(CMakePackage):
    """ecFlow is a work flow package that enables users to run a large number
    of programs (with dependencies on each other and on time) in a controlled
    environment.

    It provides tolerance for hardware and software failures, combined with
    good restart capabilities.
    """

    homepage = 'https://confluence.ecmwf.int/display/ECFLOW/'
    url      = 'https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-4.11.1-Source.tar.gz'

    maintainers = [ 'climbfuji' ]

    #https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-5.8.3-Source.tar.gz?api=v2
    version('5.8.3', sha256='1d890008414017da578dbd5a95cb1b4d599f01d5a3bb3e0297fe94a87fbd81a6')
    version('4.13.0', sha256='c743896e0ec1d705edd2abf2ee5a47f4b6f7b1818d8c159b521bdff50a403e39')
    version('4.12.0', sha256='566b797e8d78e3eb93946b923ef540ac61f50d4a17c9203d263c4fd5c39ab1d1')
    version('4.11.1', sha256='b3bcc1255939f87b9ba18d802940e08c0cf6379ca6aeec1fef7bd169b0085d6c')

    variant('static_boost', default=False,
            description='Use also static boost libraries when compiling')

    variant('ui', default=False, description='Enable ecflow_ui')

    # v4: Boost-1.7X release not working well on serialization
    depends_on('boost@1.53:1.69+python', when='@:4')
    depends_on('boost@1.53:1.69+pic', when='@:4 +static_boost')
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='@:4')

    # Use newer boost with v5
    depends_on('boost@1.72:+chrono+date_time+exception+filesystem+program_options+python+regex+serialization+system+test+thread+timer', when='@5:')
    depends_on('boost@1.72:+chrono+date_time+exception+filesystem+program_options+python+regex+serialization+system+test+thread+timer+pic', when='@5: +static_boost')

    depends_on('openssl@1:', when='@5:')
    depends_on('qt@5:', when='+ui')
    depends_on('cmake@2.12.11:', type='build')

    def cmake_args(self):
        boost_lib = self.spec['boost'].prefix.lib
        args = ['-DBoost_PYTHON_LIBRARY_RELEASE=' + boost_lib]

        ecflow_ui = 'ON' if '+ui' in self.spec else 'OFF'
        # https://jira.ecmwf.int/browse/SUP-2641#comment-208943
        use_static_boost = 'ON' if '+static_boost' in self.spec else 'OFF'
        args.append('-DENABLE_STATIC_BOOST_LIBS=' + use_static_boost)

        args.extend(['-DENABLE_UI=' + ecflow_ui, '-DENABLE_GUI=' + ecflow_ui])
        return args
