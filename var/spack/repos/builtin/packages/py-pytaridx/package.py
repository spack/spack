# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytaridx(PythonPackage):
    """Python module/library for creating and maintaining a rapidly searchable index for a tar-file. This allows "direct access" of members (files) in the tar archive."""

    homepage = "https://lc.llnl.gov/bitbucket/users/tomaso/repos/pytaridx/browse"
    git      = "ssh://git@cz-bitbucket.llnl.gov:7999/~tomaso/pytaridx.git"

    version('0.0.3', tag='v0.0.3')
    version('0.0.1',  branch='package/v0.0.1')
    version('master',  branch='master')

    depends_on('py-setuptools', type='build')
