# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCclib(PythonPackage):
    """Open source library for parsing and interpreting the results of
    computational chemistry packages"""

    homepage = "https://cclib.github.io/"

    version('1.5.post1', '1a50be48e4597b1a6dabe943da82a43c',
            url="https://github.com/cclib/cclib/releases/download/v1.5/cclib-1.5.post1.tar.gz")

    depends_on('py-numpy@1.5:', type=('build', 'run'))
