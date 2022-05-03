# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytaridx(PythonPackage):
    """Python module/library for creating and maintaining a rapidly searchable
       index for a tar-file. This allows "direct access" of members (files) in
       the tar archive."""

    homepage = "https://github.com/LLNL/pytaridx"
    git      = "https://github.com/LLNL/pytaridx.git"
    url      = "https://github.com/LLNL/pytaridx/archive/refs/tags/v1.0.2.tar.gz"

    maintainers = ['bhatiaharsh']

    version('1.0.2', sha256='b1de4d5224b61f9c5aa1edf24b4ba0bfe1c5d2eb358c7a9b7914734ffb4efe8b')
    version('master',  branch='master')

    depends_on('python@3:')
    depends_on('py-setuptools', type='build')
