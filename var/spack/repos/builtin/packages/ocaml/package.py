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


class Ocaml(Package):
    """OCaml is an industrial strength programming language supporting
       functional, imperative and object-oriented styles"""

    homepage = "http://ocaml.org/"
    url      = "http://caml.inria.fr/pub/distrib/ocaml-4.03/ocaml-4.03.0.tar.gz"

    version('4.03.0', '43812739ea1b4641cf480f57f977c149')

    depends_on('ncurses')

    def install(self, spec, prefix):
        configure('-prefix', '{0}'.format(prefix))
        
        make('world.opt')
        make('install')
