# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JsonC(AutotoolsPackage):
    """A JSON implementation in C."""
    homepage = "https://github.com/json-c/json-c/wiki"
    url      = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.12.1.tar.gz"

    version('0.13.1', '04969ad59cc37bddd83741a08b98f350')
    version('0.12.1', '55f7853f7d8cf664554ce3fa71bf1c7d')
    version('0.11',   'aa02367d2f7a830bf1e3376f77881e98')

    depends_on('autoconf', type='build')

    parallel = False

    @when('@0.12.1 %gcc@7:')
    def patch(self):
        filter_file('-Wextra',
                    '-Wextra -Wno-error=implicit-fallthrough',
                    'Makefile.in')
