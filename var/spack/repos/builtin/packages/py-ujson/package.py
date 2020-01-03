# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUjson(PythonPackage):
    """Ultra fast JSON decoder and encoder written in C with Python
       bindings."""

    homepage = "https://github.com/esnme/ultrajson"
    url      = "https://files.pythonhosted.org/packages/16/c4/79f3409bc710559015464e5f49b9879430d8f87498ecdc335899732e5377/ujson-1.35.tar.gz"

    version('1.35', sha256='f66073e5506e91d204ab0c614a148d5aa938bdbf104751be66f8ad7a222f5f86')

    depends_on('py-setuptools', type='build')
