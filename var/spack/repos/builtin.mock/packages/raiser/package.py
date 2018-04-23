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
from six.moves import builtins

from spack import *


class Raiser(Package):
    """A package that can raise a built-in exception
    of any kind with any message
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')
    version('2.0', '2.0_a_hash')

    variant(
        'exc_type',
        values=lambda x: isinstance(x, str),
        default='RuntimeError',
        description='type of the exception to be raised',
        multi=False
    )

    variant(
        'msg',
        values=lambda x: isinstance(x, str),
        default='Unknown Exception',
        description='message that will be tied to the exception',
        multi=False
    )

    def install(self, spec, prefix):
        print('Raiser will raise ')
        exc_typename = self.spec.variants['exc_type'].value
        exc_type = getattr(builtins, exc_typename)
        msg = self.spec.variants['msg'].value
        raise exc_type(msg)
