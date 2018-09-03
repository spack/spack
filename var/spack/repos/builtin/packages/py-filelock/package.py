##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class PyFilelock(PythonPackage):
    """This package contains a single module, which implements a platform
    independent file lock in Python, which provides a simple way of
    inter-process communication"""

    homepage = "https://github.com/benediktschmitt/py-filelock"
    url = "https://github.com/benediktschmitt/py-filelock/archive/v3.0.4.tar.gz"

    version('3.0.4',  '3cafce82375c3b635f2c872acaf3a00b')
    version('3.0.3',  'e4bd69f15ebcc6d5a3d684cea3694840')
    version('3.0.1',  'cbf41ad3d89c89e2b752bc85b501dff6')
    version('3.0.0',  '29d199e8998ac324d0d7cab7aa814943')
    version('2.0.13', 'cdd0c4f3e905fbab76d1202ce8e8b454')
    version('2.0.12', 'fffda24b6cfd459ea5d2d5c335e949e2')
    version('2.0.11', '9e8cbbe18494d12647050bb32a7e624d')
    version('2.0.10', '1791e72bb19e503fdd0f365fb8ce2a4d')
    version('2.0.9',  'b0269e7f77a090cc0d5fc9cf5fbe6ac2')
    version('2.0.8',  '939ec6d4e2ecdc353a1f27fc452d8e8c')
