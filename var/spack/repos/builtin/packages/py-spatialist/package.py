# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PySpatialist(PythonPackage):
    """This package offers functionalities for user-friendly geo data
    processing using GDAL and OGR."""

    homepage = "https://github.com/johntruckenbrodt/spatialist"
    url      = "https://files.pythonhosted.org/packages/source/s/spatialist/spatialist-0.2.8.tar.gz"

    version('0.2.8', sha256='97de7f9c0fbf28497ef28970bdf8093a152e691a783e7edad22998cb235154c6')

    depends_on('py-setuptools', type='build')
    depends_on('py-progressbar2', type=('build', 'run'))
    depends_on('py-pathos@0.2.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-ipywidgets', type=('build', 'run'))
    depends_on('py-tblib', type=('build', 'run'))
