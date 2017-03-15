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


class PyJinja2(PythonPackage):
    """Jinja2 is a template engine written in pure Python. It provides
    a Django inspired non-XML syntax but supports inline expressions
    and an optional sandboxed environment."""

    homepage = "http://jinja.pocoo.org/"
    url      = "https://pypi.python.org/packages/source/J/Jinja2/Jinja2-2.8.tar.gz"

    version('2.8',   'edb51693fe22c53cee5403775c71a99e')
    version('2.7.3', 'b9dffd2f3b43d673802fe857c8445b1a')
    version('2.7.2', 'df1581455564e97010e38bc792012aa5')
    version('2.7.1', '282aed153e69f970d6e76f78ed9d027a')
    version('2.7',   'c2fb12cbbb523c57d3d15bfe4dc0e8fe')

    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe', type=('build', 'run'))
    depends_on('py-babel@0.8:', type=('build', 'run'))  # optional, required for i18n
