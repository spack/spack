# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPhonopy(PythonPackage):
    """Phonopy is an open source package for phonon
    calculations at harmonic and quasi-harmonic levels."""
    homepage = "http://atztogo.github.io/phonopy/index.html"
    url      = "http://sourceforge.net/projects/phonopy/files/phonopy/phonopy-1.10/phonopy-1.10.0.tar.gz"

    version('1.10.0', '973ed1bcea46e21b9bf747aab9061ff6')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
