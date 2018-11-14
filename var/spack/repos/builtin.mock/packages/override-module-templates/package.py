# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OverrideModuleTemplates(Package):
    homepage = "http://www.fake-spack-example.org"
    url      = "http://www.fake-spack-example.org/downloads/fake-1.0.tar.gz"

    version('1.0', 'foobarbaz')

    dotkit_template = 'override.txt'
    tcl_template = 'override.txt'
    lmod_template = 'override.txt'

    def install(self, spec, prefix):
        pass
