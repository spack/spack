# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribBibtex(PythonPackage):
    """A Sphinx extension for BibTeX style citations."""

    homepage = "https://pypi.python.org/pypi/sphinxcontrib-bibtex"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-bibtex/sphinxcontrib-bibtex-0.3.5.tar.gz"

    import_modules = ['sphinxcontrib', 'sphinxcontrib.bibtex']

    version('0.3.5', sha256='c93e2b4a0d14f0ab726f95f0a33c1675965e9df3ed04839635577b8f978206cd')

    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@0.3.0:', type=('build', 'run'))
    depends_on('py-pybtex@0.17:', type=('build', 'run'))
    depends_on('py-pybtex-docutils@0.2.0:', type=('build', 'run'))
    depends_on('py-six@1.4.1:', type=('build', 'run'))
    depends_on('py-sphinx@1.0:', type=('build', 'run'))
    depends_on('py-oset@0.1.3:', type=('build', 'run'))
    depends_on('py-ordereddict@1.1:', when='^python@:2.6', type=('build', 'run'))
