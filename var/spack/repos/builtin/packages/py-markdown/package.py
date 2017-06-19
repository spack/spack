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


class PyMarkdown(PythonPackage):
    """This is a Python implementation of John Gruber's Markdown. It is
    almost completely compliant with the reference implementation, though
    there are a few very minor differences. See John's Syntax
    Documentation for the syntax rules.
    """

    homepage = "https://pythonhosted.org/Markdown/"
    url      = "https://github.com/waylan/Python-Markdown/archive/2.6.7-final.tar.gz"

    version('2.6.7', 'fd27044042e197ad99249b3d60215d97')
    version('2.6.6', '2b47a0ff7eb19ef34453fe198a0cccc4')
    version('2.6.5', 'e4b6b65b2d6bcac07176fb209bc55614')
    version('2.6.4', '5fb3cd9945eb534e71af597f8ee3622b')
    version('2.6.3', 'ec7a50ce9fd4a5fd0b24555d47e9d7d1')
    version('2.6.2', '6ce86913e9bf5bb34d9ee394ac71f044')
    version('2.6.1', '0ae69693c5adb27caf0160941d7dcbdf')
    version('2.6', '9acdde43d99847d0c4ef03ea56b1d2c5')
    version('2.5.2', 'ed2a662d22799186c1ef85d173d38b8a')
    version('2.5.1', 'be6f6ba65a8fb843d2aaf1fcdd68c755')
    version('2.5', '8393ceab9c6e33357fb8a7be063a4849')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.2:3.4')

    def url_for_version(self, version):
        base_url = "https://github.com/waylan/Python-Markdown/archive"
        return "{0}/{1}-final.tar.gz".format(base_url, version)
