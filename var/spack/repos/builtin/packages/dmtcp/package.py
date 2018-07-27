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


class Dmtcp(AutotoolsPackage):
    """DMTCP (Distributed MultiThreaded Checkpointing) transparently
    checkpoints a single-host or distributed computation in user-space --
    with no modifications to user code or to the O/S."""

    homepage = "http://dmtcp.sourceforge.net/"
    url      = "https://sourceforge.net/projects/dmtcp/files/2.5.2/dmtcp-2.5.2.tar.gz/download"

    version('2.5.2', sha256='0e3e5e15bd401b7b6937f2b678cd7d6a252eab0a143d5740b89cc3bebb4282be')
