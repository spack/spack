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
from spack import depends_on, extends, version
from spack import Package


class PyJinja2(Package):
    """
    Jinja2 is a template engine written in pure Python. It provides
    a Django inspired non-XML syntax but supports inline expressions
    and an optional sandboxed environment.
    """

    homepage = "http://jinja.pocoo.org/"
    url      = "https://github.com/pallets/jinja/archive/2.8.tar.gz"

    version('2.8', '4114200650d7630594e3bc70af23f59e')
    version('2.7.3', '55b87bdc8e585b8b5b86734eefce2621')
    version('2.7.2', '8e8f226809ae6363009b9296e30adf30')
    version('2.7.1', '69b6675553c81b1087f95cae7f2179bb')
    version('2.7', 'ec70433f325051dcedacbb2465028a35')

    extends("python")
    depends_on("py-setuptools")
    depends_on("py-markupsafe")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

