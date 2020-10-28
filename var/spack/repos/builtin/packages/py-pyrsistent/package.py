# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyrsistent(PythonPackage):
    """Pyrsistent is a number of persistent collections (by some referred to
       as functional data structures). Persistent in the sense that they are
       immutable."""

    homepage = "https://github.com/tobgu/pyrsistent"
    git      = "https://github.com/tobgu/pyrsistent.git"
    url      = "https://pypi.io/packages/source/p/pyrsistent/pyrsistent-0.16.0.tar.gz"

    version('0.16.0', sha256='28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3')

    depends_on('py-setuptools', type=('build', 'run'))
