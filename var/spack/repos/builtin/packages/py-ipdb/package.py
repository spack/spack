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


class PyIpdb(Package):
    """ipdb is the iPython debugger and has many additional features, including
    a better interactive debugging experience via colorized output."""

    homepage = "https://pypi.python.org/pypi/ipdb"
    url      = "https://pypi.io/packages/source/i/ipdb/ipdb-0.10.1.tar.gz"

    version('0.10.1', '4aeab65f633ddc98ebdb5eebf08dc713')
    # Old versions of python have conflicts, search for 'Warning' on
    # the pypi page: https://pypi.python.org/pypi/ipdb
    version('0.8',    '96dca0712efa01aa5eaf6b22071dd3ed') # python 2.5
    version('0.6',    '4a4b32e64c043522368c7871d8f50b6d') # python 2.4 or less

    def url_for_version(self, version):
        base_url = "https://pypi.io/packages/source/i/ipdb/ipdb-"
        # v0.8 was only packaged as a .zip, the others usually are .tar.gz
        # See https://pypi.python.org/simple/ipdb/
        if version == Version("0.8"):
            return "{}{}.zip".format(base_url, version)
        else:
            return "{}{}.tar.gz".format(base_url, version)

    # :TODO:
    # There might be potential to add variants here, but at the time of writing
    # this the original packager does not know what they are. See the 3rd party
    # section on ipdb's GitHub:
    #     https://github.com/gotcha/ipdb#third-party-support

    # The python dependencies below are enumerating the latest known stable for
    # earlier versions of python. The author understands these dependencies as:
    #     - Any python >= 2.5 works with 0.8 and later
    #     - Python v2.4 and earlier need 0.6 or earlier
    #     - Python 2.x should be able to compile 0.6,
    #       but 3.x can only compile 0.8+
    # Thanks @adamjstewart for help with the dependencies :)
    # Future editors should not add _earlier_ versions or the following logic
    # may not be valid anymore!
    extends('python')
    depends_on('python@2.6:2.7,3.2:', when='@0.9.1:0.10.1')
    depends_on('python@2.5:2.7,3.2.0:3.2.999', when='@0.7:0.9.0')
    depends_on('python@2.4:2.7', when='@:0.6.1')

    # Dependencies gathered from: https://github.com/gotcha/ipdb/blob/master/setup.py
    depends_on('py-setuptools', type='build')
    depends_on('py-ipython',    type=('build', 'link'))# ipdb needs ipython to run

    def install(self, spec, prefix):
        # Installation is uncomplicated, this should suffice.
        setup_py('install', '--prefix={0}'.format(prefix))
