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


class PyBeautifulsoup4(PythonPackage):
    """Beautiful Soup is a Python library for pulling data out of HTML and
    XML files. It works with your favorite parser to provide idiomatic ways
    of navigating, searching, and modifying the parse tree."""

    homepage = "https://www.crummy.com/software/BeautifulSoup"
    url = "https://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-4.4.1.tar.gz"

    version('4.5.1', '994abd90e691beaf7d42c00ffb2f3a67',
            url='https://www.crummy.com/software/BeautifulSoup/bs4/'
            'download/4.5/beautifulsoup4-4.5.1.tar.gz')
    version('4.4.1', '8fbd9a7cac0704645fa20d1419036815')

    depends_on('py-setuptools', type='build')
