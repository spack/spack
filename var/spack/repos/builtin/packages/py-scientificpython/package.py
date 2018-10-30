# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyScientificpython(PythonPackage):
    """ScientificPython is a collection of Python modules for
       scientific computing. It contains support for geometry,
       mathematical functions, statistics, physical units, IO,
       visualization, and parallelization."""

    homepage = "https://sourcesup.renater.fr/projects/scientific-py/"
    url      = "https://sourcesup.renater.fr/frs/download.php/file/4411/ScientificPython-2.8.1.tar.gz"
    version('2.8.1', '73ee0df19c7b58cdf2954261f0763c77')

    depends_on('py-numpy', type=('build', 'run'))
