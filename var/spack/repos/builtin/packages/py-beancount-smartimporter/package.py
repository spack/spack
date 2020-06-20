# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBeancountSmartimporter(PythonPackage):
    """Augment Beancount importers with machine learning functionality."""

    homepage = "https://github.com/beancount/smart_importer"
    url      = "https://github.com/beancount/smart_importer/archive/v0.1.tar.gz"
    git      = "git@github.com:beancount/smart_importer.git"

    version('master', branch='master')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
    depends_on('py-pytest', type=('test'))

    depends_on('py-beancount@2.0.0:',    type=('build', 'run'))
    depends_on('py-numpy@1.8.2:',        type=('build', 'run'))
    depends_on('py-scikit-learn@0.19:',  type=('build', 'run'))
    depends_on('py-scipy@0.13.3:',       type=('build', 'run'))
