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


class PySphinxcontribBibtex(PythonPackage):
    """A Sphinx extension for BibTeX style citations."""

    homepage = "https://pypi.python.org/pypi/sphinxcontrib-bibtex"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-bibtex/sphinxcontrib-bibtex-0.3.5.tar.gz"

    import_modules = ['sphinxcontrib', 'sphinxcontrib.bibtex']

    version('0.3.5', 'd3c86836e2f6227b55a5ca9108590b1c')

    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@0.3.0:', type=('build', 'run'))
    depends_on('py-pybtex@0.17:', type=('build', 'run'))
    depends_on('py-pybtex-docutils@0.2.0:', type=('build', 'run'))
    depends_on('py-six@1.4.1:', type=('build', 'run'))
    depends_on('py-sphinx@1.0:', type=('build', 'run'))
    depends_on('py-oset@0.1.3:', type=('build', 'run'))
    depends_on('py-ordereddict@1.1:', when='^python@:2.6', type=('build', 'run'))
