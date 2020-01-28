# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPybtex(PythonPackage):
    """Pybtex is a BibTeX-compatible bibliography processor written in
       Python."""

    homepage = "https://pybtex.org"
    url      = "https://pypi.io/packages/source/P/Pybtex/pybtex-0.21.tar.gz"

    import_modules = [
        'custom_fixers', 'pybtex', 'pybtex.style', 'pybtex.tests',
        'pybtex.database', 'pybtex.backends', 'pybtex.bibtex',
        'pybtex.charwidths', 'pybtex.markup', 'pybtex.plugin',
        'pybtex.style.sorting', 'pybtex.style.names',
        'pybtex.style.labels', 'pybtex.style.formatting',
        'pybtex.tests.database_test', 'pybtex.tests.bst_parser_test',
        'pybtex.tests.data', 'pybtex.database.output',
        'pybtex.database.input', 'pybtex.database.format',
        'pybtex.database.convert'
    ]

    version('0.21', sha256='af8a6c7c74954ad305553b118d2757f68bc77c5dd5d5de2cc1fd16db90046000')

    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@1.0.4:', type=('build', 'run'))
    depends_on('py-pyyaml@3.01:', type=('build', 'run'))
    depends_on('py-counter@1:', when='^python@:2.6', type=('build', 'run'))
