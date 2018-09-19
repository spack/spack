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


class PyDocutils(PythonPackage):
    """Docutils is an open-source text processing system for processing
    plaintext documentation into useful formats, such as HTML, LaTeX,
    man-pages, open-document or XML. It includes reStructuredText, the
    easy to read, easy to use, what-you-see-is-what-you-get plaintext
    markup language."""

    homepage = "http://docutils.sourceforge.net/"
    url      = "https://pypi.io/packages/source/d/docutils/docutils-0.13.1.tar.gz"

    import_modules = [
        'docutils', 'docutils.languages', 'docutils.parsers',
        'docutils.readers', 'docutils.transforms', 'docutils.utils',
        'docutils.writers', 'docutils.parsers.rst',
        'docutils.parsers.rst.directives', 'docutils.parsers.rst.languages',
        'docutils.utils.math', 'docutils.writers.html4css1',
        'docutils.writers.html5_polyglot', 'docutils.writers.latex2e',
        'docutils.writers.odf_odt', 'docutils.writers.pep_html',
        'docutils.writers.s5_html', 'docutils.writers.xetex'
    ]

    version('0.13.1', 'ea4a893c633c788be9b8078b6b305d53')
    version('0.12',   '4622263b62c5c771c03502afa3157768')
