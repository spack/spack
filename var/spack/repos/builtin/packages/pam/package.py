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


class Pam(AutotoolsPackage):
    """Linux Pluggable Authentication Modules"""

    homepage = "http://linux-pam.org/"
    url      = "http://linux-pam.org/library/Linux-PAM-1.3.0.tar.bz2"

    version('1.3.0', 'da4b2289b7cfb19583d54e9eaaef1c3a')
    version('1.2.1', '9dc53067556d2dd567808fd509519dd6')
    version('1.2.0', 'ee4a480d77b341c99e8b1375f8f180c0')

    def configure_args(self):
        prefix = self.spec.prefix
        return [
            '--includedir={0}/include/security'.format(prefix)]
