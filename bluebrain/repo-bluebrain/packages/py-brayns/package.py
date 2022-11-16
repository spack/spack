# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrayns(PythonPackage):
    """Python client to the Brayns renderer"""

    homepage = "https://github.com/BlueBrain/Brayns"
    git = "https://github.com/BlueBrain/Brayns.git"
    pypi = "brayns/brayns-3.0.0.tar.gz"

    submodules = False

    build_directory = 'python'

    version('develop', branch='develop')
    version('3.0.0', tag='3.0.0')

    depends_on('py-websockets@10.3')
    depends_on('python@3.9:')
