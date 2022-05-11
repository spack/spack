# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class PyOpencensusContext(PythonPackage):
    """OpenCensus Runtime Context."""

    homepage = "https://github.com/census-instrumentation/opencensus-python/tree/master/context/opencensus-context"
    url      = "https://pypi.io/packages/py2.py3/o/opencensus-context/opencensus_context-0.1.1-py2.py3-none-any.whl"

    version('0.1.1', sha256='1a3fdf6bec537031efcc93d51b04f1edee5201f8c9a0c85681d63308b76f5702', expand=False)

    depends_on('py-contextvars', when='^python@3.6.0:3.6', type=('build', 'run'))
