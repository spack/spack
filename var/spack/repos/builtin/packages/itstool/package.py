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


class Itstool(AutotoolsPackage):
    """ITS Tool allows you to translate your XML documents with PO files, using
       rules from the W3C Internationalization Tag Set (ITS) to determine what
       to translate and how to separate it into PO file messages."""

    homepage = "http://itstool.org/"
    url      = "http://files.itstool.org/itstool/itstool-2.0.2.tar.bz2"

    version('2.0.2', 'd472d877a7bc49899a73d442085b2f93')
    version('2.0.1', '40935cfb08228488bd45575e5f001a34')
    version('2.0.0', 'd8c702c3e8961db83d04182c2aa4730b')
    version('1.2.0', 'c0925f6869e33af8e7fe56848c129152')
