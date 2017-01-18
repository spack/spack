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


class Libmonitor(AutotoolsPackage):
    """Libmonitor is a library for process and thread control."""
    homepage = "https://github.com/HPCToolkit/libmonitor"
    version('20130218', git='https://github.com/HPCToolkit/libmonitor.git',
            commit='4f2311e')
    variant('krellpatch', default=False,
            description="build with openspeedshop based patch.")

    patch('libmonitorkrell-0000.patch', when='@20130218+krellpatch')
    patch('libmonitorkrell-0001.patch', when='@20130218+krellpatch')
    patch('libmonitorkrell-0002.patch', when='@20130218+krellpatch')
