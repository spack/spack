# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribQthelp(PythonPackage):
    """sphinxcontrib-qthelp is a sphinx extension which outputs QtHelp
    document."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-qthelp/sphinxcontrib-qthelp-1.0.2.tar.gz"

    version('1.0.2', sha256='79465ce11ae5694ff165becda529a600c754f4bc459778778c7017374d4d406f')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
