# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Direnv(Package):
    """direnv is an environment switcher for the shell."""

    homepage = "https://direnv.net/"
    url      = "https://github.com/direnv/direnv/archive/v2.11.3.tar.gz"

    maintainers = ['acastanedam']

    version('2.30.2', sha256='a2ee14ebdbd9274ba8bf0896eeb94e98947a056611058dedd4dbb43167e076f3')
    version('2.20.0', sha256='cc72525b0a5b3c2ab9a52a3696e95562913cd431f923bcc967591e75b7541bff')
    version('2.11.3', sha256='2d34103a7f9645059270763a0cfe82085f6d9fe61b2a85aca558689df0e7b006')

    depends_on('go', type='build')

    def install(self, spec, prefix):
        make('install', "PREFIX=%s" % prefix)
