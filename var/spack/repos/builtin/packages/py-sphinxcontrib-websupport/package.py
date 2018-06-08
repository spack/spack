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


class PySphinxcontribWebsupport(PythonPackage):
    """sphinxcontrib-webuspport provides a Python API to easily integrate
    Sphinx documentation into your Web application."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-websupport/sphinxcontrib-websupport-1.0.1.tar.gz"

    # FIXME: These import tests don't work for some reason
    # import_modules = [
    #     'sphinxcontrib', 'sphinxcontrib.websupport',
    #     'sphinxcontrib.websupport.storage', 'sphinxcontrib.websupport.search'
    # ]

    version('1.0.1', '84df26463b1ba65b07f926dbe2055665')

    depends_on('py-setuptools', type='build')

    depends_on('py-pytest', type='test')
    depends_on('py-mock',   type='test')
