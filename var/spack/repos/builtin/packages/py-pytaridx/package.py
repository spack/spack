# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytaridx(PythonPackage):
    """Python module/library for creating and maintaining a rapidly searchable index for a tar-file. This allows "direct access" of members (files) in the tar archive."""

    homepage = "https://github.com/LLNL/pytaridx"
    git      = "git@github.com:LLNL/pytaridx.git"

    version('main',  branch='main')

    depends_on('python@3:')
    depends_on('py-setuptools', type='build')
