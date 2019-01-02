# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtml5lib(PythonPackage):
    """HTML parser based on the WHATWG HTML specification."""

    homepage = "https://github.com/html5lib/html5lib-python"
    url      = "https://pypi.io/packages/source/h/html5lib/html5lib-0.9999999.tar.gz"

    version('0.9999999', 'ef43cb05e9e799f25d65d1135838a96f')

    depends_on('python@2.6:2.8,3.2:3.4')
    depends_on('py-six', type=('build', 'run'))
