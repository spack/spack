# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ecflow(CMakePackage):
    """ecFlow is a work flow package that enables users to run a large number
    of programs (with dependencies on each other and on time) in a controlled
    environment.

    It provides tolerance for hardware and software failures, combined with
    good restart capabilities.
    """

    homepage = 'https://confluence.ecmwf.int/display/ECFLOW/'
    url      = 'https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-4.11.1-Source.tar.gz'

    version('4.11.1', sha256='b3bcc1255939f87b9ba18d802940e08c0cf6379ca6aeec1fef7bd169b0085d6c')

    variant('static_boost', default=False,
            description='Use also static boost libraries when compiling')

    depends_on('boost+python')
    depends_on('boost+pic', when='+static_boost')
    depends_on('qt')
    depends_on('cmake@2.8.11:', type='build')

    def cmake_args(self):
        boost_lib = self.spec['boost'].prefix.lib
        args = ['-DBoost_PYTHON_LIBRARY_RELEASE=' + boost_lib]

        # https://jira.ecmwf.int/browse/SUP-2641#comment-208943
        use_static_boost = 'ON' if '+static_boost' in self.spec else 'OFF'
        args.append('-DENABLE_STATIC_BOOST_LIBS=' + use_static_boost)

        return args
