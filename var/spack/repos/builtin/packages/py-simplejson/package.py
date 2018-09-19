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


class PySimplejson(PythonPackage):
    """Simplejson is a simple, fast, extensible JSON encoder/decoder for
    Python"""

    homepage = "https://github.com/simplejson/simplejson"
    url      = "https://pypi.io/packages/source/s/simplejson/simplejson-3.10.0.tar.gz"

    version('3.10.0', '426a9631d22851a7a970b1a677368b15')
    version('3.9.0',  '01db2db1b96bd8e59bcab45bca12639b')
    version('3.8.2',  '53b1371bbf883b129a12d594a97e9a18')
    version('3.8.1',  'b8441f1053edd9dc335ded8c7f98a974')
    version('3.8.0',  '72f3b93a6f9808df81535f79e79565a2')

    depends_on('py-setuptools', type='build')
