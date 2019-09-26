# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ctffind(AutotoolsPackage):
    """Fast and accurate defocus estimation from electron micrographs."""

    homepage = "http://grigoriefflab.janelia.org/ctffind4"
    url      = "http://grigoriefflab.janelia.org/sites/default/files/ctffind-4.1.8.tar.gz"

    version('4.1.8', '8ae9d9abe363141a3792981b5a2fae94')

    depends_on('wxwidgets')
    depends_on('fftw@3:')
