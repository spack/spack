# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLdap(PythonPackage):
    """python-ldap provides an object-oriented API to access LDAP directory
    servers from Python programs.
    """

    homepage = "https://www.python-ldap.org/en/python-ldap-3.2.0/"
    url      = "https://files.pythonhosted.org/packages/source/p/python-ldap/python-ldap-3.2.0.tar.gz"

    version('3.2.0', sha256='7d1c4b15375a533564aad3d3deade789221e450052b21ebb9720fb822eccdb8e')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-pyasn1', type='run')
    depends_on('py-pyasn1-modules', type='build')
