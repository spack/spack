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


class UrlOnlyOverrideWithGaps(Package):
    homepage = 'http://www.example.com'

    version('1.0.5', 'abcdef0')
    version('1.0.0', 'bcdef0a', url='http://a.example.com/url_override-1.0.0.tar.gz')
    version('0.9.5', 'cdef0ab')
    version('0.9.0', 'def0abc', url='http://b.example.com/url_override-0.9.0.tar.gz')
    version('0.8.5', 'ef0abcd')
    version('0.8.1', 'f0abcde', url='http://c.example.com/url_override-0.8.1.tar.gz')
    version('0.7.0', '0abcdef')
