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
from spack.architecture import Platform, Target
from spack.architecture import OperatingSystem as OS


class Test(Platform):
    priority    = 1000000
    front_end   = 'x86_32'
    back_end    = 'x86_64'
    default     = 'x86_64'

    front_os = 'redhat6'
    back_os = 'debian6'
    default_os = 'debian6'

    def __init__(self):
        super(Test, self).__init__('test')
        self.add_target(self.default, Target(self.default))
        self.add_target(self.front_end, Target(self.front_end))

        self.add_operating_system(self.default_os, OS('debian', 6))
        self.add_operating_system(self.front_os, OS('redhat', 6))

    @classmethod
    def detect(self):
        return True
