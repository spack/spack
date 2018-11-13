# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXattr(PythonPackage):
    """A python interface to access extended file attributes,
        sans libattr dependency"""

    homepage = "http://pyxattr.k1024.org/"
    git      = "https://github.com/fwang2/pyxattr.git"

    version('develop', branch='dev')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
