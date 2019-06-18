# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtml5lib(PythonPackage):
    """HTML parser based on the WHATWG HTML specification."""

    homepage = "https://github.com/html5lib/html5lib-python"
    url      = "https://pypi.io/packages/source/h/html5lib/html5lib-1.0.1.tar.gz"

    version('1.0.1', '942a0688d6bdf20d087c9805c40182ad')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type=('run'))
