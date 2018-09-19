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


class RPbdzmq(RPackage):
    """'ZeroMQ' is a well-known library for high-performance asynchronous
    messaging in scalable, distributed applications. This package provides
    high level R wrapper functions to easily utilize 'ZeroMQ'. We mainly focus
    on interactive client/server programming frameworks. For convenience, a
    minimal 'ZeroMQ' library (4.1.0 rc1) is shipped with 'pbdZMQ', which can
    be used if no system installation of 'ZeroMQ' is available. A few wrapper
    functions compatible with 'rzmq' are also provided."""

    homepage = "http://r-pbd.org/"
    url      = "https://cran.r-project.org/src/contrib/pbdZMQ_0.2-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pbdZMQ"

    version('0.2-4', 'e5afb70199aa54d737ee7a0e26bde060')

    depends_on('r-r6', type=('build', 'run'))
    depends_on('zeromq')
