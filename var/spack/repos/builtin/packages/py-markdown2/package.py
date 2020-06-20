# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMarkdown2(PythonPackage):
    """A fast and complete Python implementation of Markdown."""

    homepage = "https://github.com/trentm/python-markdown2"
    url      = "https://pypi.io/packages/source/m/markdown2/markdown2-2.3.9.tar.gz"

    version('2.3.9',  sha256='89526090907ae5ece66d783c434b35c29ee500c1986309e306ce2346273ada6a')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('py-pytest',           type='test')
