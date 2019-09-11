# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonMapnik(PythonPackage):
    """
    Python bindings for mapnik
    """

    homepage = "https://github.com/mapnik/python-mapnik"
    url      = "https://github.com/mapnik/python-mapnik/archive/v3.0.16.tar.gz"

    version('3.0.16', sha256='643117752fa09668a1e26a360d13cd137329ae2013eb14ad92ab72fbc479fc70')
    version('3.0.13', sha256='ced684745e778c0cac0edba89c09c6f9b9f1db18fc12744ed4710a88b78a3389')

    depends_on('py-setuptools', type='build')
    depends_on('mapnik ^boost+python+thread', type=('build', 'link', 'run'))

    # Package can't find boost_python without the following
    def setup_environment(self, spack_env, run_env):
        # Since spack installed boost lib is like libboost_python27..
        # Communicate this to package via BOOST_PYTHON_LIB='boost_python27'
        # Package expects 'boost_python2.7' by default
        py_ver = str(self.spec['python'].version.up_to(2))
        py_ver.replace('.','')
        spack_env.set('BOOST_PYTHON_LIB', 'boost_python' + py_ver)
