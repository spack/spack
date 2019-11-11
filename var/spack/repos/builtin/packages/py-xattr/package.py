# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyXattr(PythonPackage):
    """A python interface to access extended file attributes,
    sans libattr dependency.
    """

    homepage = "http://pyxattr.k1024.org/"
    git      = "https://github.com/iustin/pyxattr.git"

    version('master', branch='master')

    depends_on('python@2.7:')
    depends_on('py-setuptools', type='build')
