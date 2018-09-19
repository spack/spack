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


class Scala(Package):
    """Scala is a general-purpose programming language providing support for
    functional programming and a strong static type system. Designed to be
    concise, many of Scala's design decisions were designed to build from
    criticisms of Java.
    """

    homepage = "https://www.scala-lang.org/"
    url = "https://downloads.lightbend.com/scala/2.12.1/scala-2.12.1.tgz"

    version('2.12.5', '25cf4989d061c585bd0a3fa357ccf0a6')
    version('2.12.1', '3eaecbce019b0fa3067503846e292b32')
    version('2.11.11', '3f5b76001f60cbc31111ddb81de5ea07')
    version('2.10.6', 'd79dc9fdc627b73289306bdaec81ca98')

    depends_on('java')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('lib')
        install_dir('doc')
        install_dir('man')
