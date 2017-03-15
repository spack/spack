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


class PyProtobuf(PythonPackage):
    """Protocol buffers are Google's language-neutral, platform-neutral,
    extensible mechanism for serializing structured data - think XML, but
    smaller, faster, and simpler. You define how you want your data to be
    structured once, then you can use special generated source code to easily
    write and read your structured data to and from a variety of data streams
    and using a variety of languages."""

    homepage = 'https://developers.google.com/protocol-buffers/'
    url      = 'https://pypi.python.org/packages/source/p/protobuf/protobuf-3.0.0b2.tar.gz'

    version('3.0.0b2', 'f0d3bd2394345a9af4a277cd0302ae83')
    version('2.6.1', '6bf843912193f70073db7f22e2ea55e2')
    version('2.5.0', '338813f3629d59e9579fed9035ecd457')
    version('2.4.1', '72f5141d20ab1bcae6b1e00acfb1068a')
    version('2.3.0', 'bb020c962f252fe81bfda8fb433bafdd')

    depends_on('py-setuptools', type='build')
