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


class PyPyutilib(PythonPackage):
    """The PyUtilib project supports a collection of Python utilities,
    including a well-developed component architecture and extensions to the
    PyUnit testing framework. PyUtilib has been developed to support several
    Python-centric projects, especially Pyomo. PyUtilib is available under the
    BSD License."""

    homepage = "https://github.com/PyUtilib/pyutilib"
    url      = "https://github.com/PyUtilib/pyutilib/archive/5.5.1.tar.gz"

    version('5.6.2', '60c6ea5083e512211984347ffeca19d2')
    version('5.6.1', 'ddc7e896304b6fabe4d21eb5fdec386e')
    version('5.6',   '5bfcdbf118264f1a1b8c6cac9dea8bca')
    version('5.5.1', 'c4990cbced152d879812d109aaa857ff')
    version('5.5',   '7940563bf951332cf836f418d67b2134')
    version('5.4.1', 'b34b5798757e4ab73868b7655c5c8f8a')
    version('5.4',   '9410e5a76885412310b03074d2f97e55')
    version('5.3.5', '85e41e65f24f6711261229bcde6eb825')
    version('5.3.4', '4fe1a8387c027f64b62ca99424275368')
    version('5.3.3', '27a713ca8d49714244646e1ce38778b9')

    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
