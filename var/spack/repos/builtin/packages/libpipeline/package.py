# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpipeline(AutotoolsPackage):
    """libpipeline is a C library for manipulating pipelines of subprocesses
    in a flexible and convenient way."""

    homepage = "http://libpipeline.nongnu.org/"
    git = "https://gitlab.com/cjwatson/libpipeline"
    url = "https://download.savannah.nongnu.org/releases/libpipeline/libpipeline-1.5.5.tar.gz"

    version('1.5.5', sha256='0c8367f8b82bb721b50647a647115b6e62a37e3b2e954a9685e4d933f30c00cc')
    version('1.4.2', sha256='fef1fc9aa40ce8796f18cd1aecd888a9484a9556c8b0f8d07c863578277679be')

    depends_on('pkgconfig', type='build')
    depends_on('check', type='test')
