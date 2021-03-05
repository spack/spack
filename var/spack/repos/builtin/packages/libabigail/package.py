# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libabigail(AutotoolsPackage):
    """The ABI Generic Analysis and Instrumentation Library"""

    homepage = "https://sourceware.org/libabigail"
    url      = "https://mirrors.kernel.org/sourceware/libabigail/libabigail-1.8.tar.gz"

    version('1.8', sha256='1cbf260b894ccafc61b2673ba30c020c3f67dbba9dfa88dca3935dff661d665c')

    depends_on('doxygen', type='build')
    depends_on('elfutils', type=('build', 'link'))
    depends_on('libdwarf')
    depends_on('libxml2')
    depends_on('py-sphinx', type='build')
