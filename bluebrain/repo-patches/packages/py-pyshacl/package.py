# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPyshacl(PythonPackage):
    """A Python validator for SHACL.
    """

    homepage = "https://github.com/RDFLib/pySHACL"
    pypi = "pyshacl/pyshacl-0.11.6.post1.tar.gz"

    version('0.17.2', sha256='46f31c7a7f7298aa5b483d92dbc850ff79a144d26f1f41e83267ed84b4d6ae23')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-rdflib@6.0.0:6.999', type=('build', 'run'))
    depends_on('py-owlrl@5.2.3:6.999', type=('build', 'run'))
    depends_on('py-prettytable@2.2.1:2', type=('build', 'run'))
