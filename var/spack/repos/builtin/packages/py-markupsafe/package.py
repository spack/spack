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


class PyMarkupsafe(Package):
    """
    MarkupSafe is a library for Python that implements a unicode
    string that is aware of HTML escaping rules and can be used
    to implement automatic string escaping. It is used by Jinja 2,
    the Mako templating engine, the Pylons web framework and many more.
    """

    homepage = "http://www.pocoo.org/projects/markupsafe/"
    url      = "https://github.com/pallets/markupsafe/archive/0.23.tar.gz"

    version('0.23', '1a0dadc95169832367c9dcf142155cde')
    version('0.22', '7a2ac7427b58def567628d06dc328396')
    version('0.21', 'aebcd93ee05269773c8b80bb6c86fc2f')
    version('0.20', '0c1fef97c8fd6a986d708f08d7f84a02')
    version('0.19', '64b05361adb92c11839fc470e308c593')

    extends("python")
    depends_on("py-setuptools")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

