# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWrapt(PythonPackage):
    """Module for decorators, wrappers and monkey patching."""

    homepage = "https://github.com/GrahamDumpleton/wrapt"
    url      = "https://pypi.io/packages/source/w/wrapt/wrapt-1.10.10.tar.gz"

    version('1.10.10', '97365e906afa8b431f266866ec4e2e18')
