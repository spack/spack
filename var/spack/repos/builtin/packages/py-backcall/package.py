# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBackcall(PythonPackage):
    """Specifications for callback functions passed in to an API"""

    homepage = "https://github.com/takluyver/backcall"
    url = "https://pypi.io/packages/source/b/backcall/backcall-0.1.0.tar.gz"

    version('0.1.0', '87ce0c7839808e6a3427d57df6a792e7')
