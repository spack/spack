# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libabigail(AutotoolsPackage):
    """The ABI Generic Analysis and Instrumentation Library"""

    homepage = "https://sourceware.org/libabigail"
    url      = "https://mirrors.kernel.org/sourceware/libabigail/libabigail-2.0.tar.gz"
    git      = "https://sourceware.org/git/libabigail.git"

    version('master')
    version('2.0', sha256='3704ae97a56bf076ca08fb5dea6b21db998fbbf14c4f9de12824b78db53b6fda')
    version('1.8', sha256='1cbf260b894ccafc61b2673ba30c020c3f67dbba9dfa88dca3935dff661d665c')

    variant('docs', default=False, description='build documentation')

    # version 2.0 will error because of using an old symbol, this error
    # libdw: dwarf.h corrected the DW_LANG_PLI constant name (was DW_LANG_PL1).
    depends_on('elfutils', type=('build', 'link'))

    depends_on('libdwarf')
    depends_on('libxml2')

    # Libabigail won't generate it's bin without Python
    depends_on('python@3.8:')

    # Documentation dependencies
    depends_on('doxygen', type="build", when="+docs")
    depends_on('py-sphinx', type='build', when="+docs")

    # The symbol PL1 needs to be renamed to PLI
    patch("0001-plt.patch")

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        with working_dir(self.configure_directory):
            autoreconf('-ivf')
