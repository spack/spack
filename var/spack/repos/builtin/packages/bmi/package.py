# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class Bmi(AutotoolsPackage):
    """a communications framework and network abstraction layer"""

    homepage = 'https://github.com/radix-io/bmi/'
    git = 'https://github.com/radix-io/bmi.git'
    url = 'https://github.com/radix-io/bmi/archive/v2.8.1.tar.gz'

    maintainers = ['carns']

    version('main', branch='main')
    version('2.8.1', sha256='28aa4341f0456cf20ee762f712d7c749ab8f864003329f9327c18ea03fc7ffdb')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')

    # need to override 'autoreconf' so we can run BMI's 'prepare' script
    def autoreconf(self, spec, prefix):
        Executable('./prepare')()

    def configure_args(self):
        args = ["--enable-shared", "--enable-bmi-only"]
        return args
