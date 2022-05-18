# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWurlitzer(PythonPackage):
    """Capture C-level stdout/stderr pipes in Python via os.dup2."""

    homepage = "https://github.com/minrk/wurlitzer"
    pypi     = "wurlitzer/wurlitzer-3.0.2.tar.gz"

    version('3.0.2', sha256='36051ac530ddb461a86b6227c4b09d95f30a1d1043de2b4a592e97ae8a84fcdf')

    depends_on('py-setuptools', type='build')
