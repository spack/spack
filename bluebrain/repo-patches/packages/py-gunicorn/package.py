# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGunicorn(PythonPackage):
    """WSGI HTTP Server for UNIX."""

    homepage = "https://pypi.org/project/gunicorn/"
    url = "https://files.pythonhosted.org/packages/28/5b/0d1f0296485a6af03366604142ea8f19f0833894db3512a40ed07b2a56dd/gunicorn-20.1.0.tar.gz"

    version('20.1.0', sha256='e0a968b5ba15f8a328fdfd7ab1fcb5af4470c28aaf7e55df02a99bc13138e6e8')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools@3.0:', type='build')
