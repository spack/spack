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


class Random123(Package):
    """Random123 is a library of 'counter-based' random number
    generators (CBRNGs), in which the Nth random number can be obtained
    by applying a stateless mixing function to N instead of the
    conventional approach of using N iterations of a stateful
    transformation."""
    homepage = "http://www.deshawresearch.com/resources_random123.html"
    url      = "http://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.09.tar.gz"

    version('1.09', '67ae45ff94b12acea590a6aa04ed1123')

    def install(self, spec, prefix):
        # Random123 doesn't have a build system.
        # We have to do our own install here.
        install_tree('include', prefix.include)
        install('./LICENSE', "%s" % prefix)
