# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCleanText(PythonPackage):
    """User-generated content on the Web and in social media is
    often dirty. Preprocess your scraped data with clean-text
    to create a normalized text representation."""

    pypi     = "clean-text/clean-text-0.5.0.tar.gz"

    version('0.5.0', sha256='e525951bef0c8b72e03c987fdac2c475b61d7debf7a8834366fd75716179b6e1')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-emoji', type=('build', 'run'))
    depends_on('py-ftfy@6.0:6.999', type=('build', 'run'))
