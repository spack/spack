##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
    url      = "https://pypi.python.org/packages/source/d/docutils/docutils-0.12.tar.gz"

    version('0.13.1', 'ea4a893c633c788be9b8078b6b305d53',
            url="https://pypi.python.org/packages/05/25/7b5484aca5d46915493f1fd4ecb63c38c333bd32aa9ad6e19da8d08895ae/docutils-0.13.1.tar.gz")
    version('0.12',   '4622263b62c5c771c03502afa3157768')
