# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ssht(Package):
    """The SSHT code provides functionality to perform fast and exact
    spin spherical harmonic transforms."""

    homepage = "https://astro-informatics.github.io/ssht/"
    git      = "https://github.com/astro-informatics/ssht.git"

    version('1.2b1', commit='7378ce8853897cbd1b08adebf7ec088c1e40f860')

    depends_on('fftw')

    def install(self, spec, prefix):
        make('default')
        install_tree('include/c', join_path(prefix, 'include'))
        install_tree('doc/c', join_path(prefix, 'doc'))
        install_tree('lib/c', join_path(prefix, 'lib'))
