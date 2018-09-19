##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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

    version('0.21', 'e7b320b2bcb34c664c4385533a2ea831')

    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@1.0.4:', type=('build', 'run'))
    depends_on('py-pyyaml@3.01:', type=('build', 'run'))
    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-counter@1:', when='^python@:2.6', type=('build', 'run'))
