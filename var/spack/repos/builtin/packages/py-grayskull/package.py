# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGrayskull(PythonPackage):
    """Project to generate recipes for conda packages."""

    homepage = "https://github.com/conda-incubator/grayskull"
    pypi     = "grayskull/grayskull-0.9.1.tar.gz"

    version('0.9.1', sha256='d3b4714479019d02ba80b66ceaaa91f562245649dd239b3070aaa9b5b99a8b86')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-ruamel-yaml@0.16.10:', type=('build', 'run'))
    depends_on('py-ruamel-yaml-jinja2', type=('build', 'run'))
    depends_on('py-stdlib-list', type=('build', 'run'))
    depends_on('py-pip', type=('build', 'run'))
    depends_on('py-setuptools@30.3:', type=('build', 'run'))
    depends_on('py-rapidfuzz@1.7.1:', type=('build', 'run'))
    depends_on('py-progressbar2@3.53:', type=('build', 'run'))
    depends_on('py-colorama', type=('build', 'run'))
