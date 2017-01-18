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


class PyIpdb(PythonPackage):
    """ipdb is the iPython debugger and has many additional features, including
    a better interactive debugging experience via colorized output."""

    homepage = "https://pypi.python.org/pypi/ipdb"
    url      = "https://pypi.io/packages/source/i/ipdb/ipdb-0.10.1.tar.gz"

    version('0.10.1', '4aeab65f633ddc98ebdb5eebf08dc713')

    # :TODO:
    # There might be potential to add variants here, but at the time of writing
    # this the original packager does not know what they are. See the 3rd party
    # section on ipdb's GitHub:
    #     https://github.com/gotcha/ipdb#third-party-support
    depends_on('python@2.6:2.7,3.2:')

    # Dependencies gathered from:
    #     https://github.com/gotcha/ipdb/blob/master/setup.py
    # However additional dependencies added below were found via testing.
    depends_on('py-setuptools',      type='build')
    # ipdb needs iPython and others available at runtime
    depends_on('py-ipython@0.10.2:', type=('build', 'link'))
    depends_on('py-traitlets',       type=('build', 'link'))
    depends_on('py-six',             type=('build', 'link'))
    depends_on('py-pexpect',         type=('build', 'link'))
    depends_on('py-prompt-toolkit',  type=('build', 'link'))
