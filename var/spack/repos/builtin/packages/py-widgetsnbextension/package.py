# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWidgetsnbextension(PythonPackage):
    """IPython HTML widgets for Jupyter"""

    homepage = "https://pypi.python.org/pypi/widgetsnbextension"
    url      = "https://pypi.io/packages/source/w/widgetsnbextension/widgetsnbextension-1.2.6.tar.gz"

    version('1.2.6', '0aa4e152c9ba2d704389dc2453f448c7')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-jupyter-notebook@4.2.0:', type=('build', 'run'))
