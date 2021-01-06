# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCheetah(PythonPackage):
    """Cheetah is a template engine and code generation tool."""

    pypi = "Cheetah/Cheetah-2.3.0.tar.gz"

    version('2.3.0', sha256='2a32d7f7f70be98c2d57aa581f979bc799d4bf17d09fc0e7d77280501edf3e53')
