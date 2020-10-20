# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGosam(PythonPackage):
    """The package GoSam allows for the automated calculation of one-loop amplitudes
       for multi-particle processes in renormalizable quantum field theories."""

    homepage = "https://gosam.hepforge.org"
    url      = "https://gosam.hepforge.org/downloads/?f=gosam-2.0.4-6d9f1cba.tar.gz"

    version('2.0.4', sha256='faf621c70f66d9dffc16ac5cce66258067f39f686d722a4867eeb759fcde4f44')
    patch('gosam-1.2.4.patch')

    depends_on('form', type=('build', 'run'))
    depends_on('qgraf', type=('build', 'run'))
    depends_on('gosam-contrib', type=('build', 'run'))
