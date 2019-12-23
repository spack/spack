# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUjson(PythonPackage):
    """Ultra fast JSON decoder and encoder written in C with Python
       bindings."""

    homepage = "https://github.com/esnme/ultrajson"
    url      = "https://github.com/esnme/ultrajson/archive/v1.35.tar.gz"

    version('1.35', sha256='1e7761583065873bed8466a3692fa5539d4f15bebc7af1c8fcc63d322a46804f')
