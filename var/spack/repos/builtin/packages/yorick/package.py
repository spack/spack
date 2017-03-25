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
import os
import shutil
import glob


class Yorick(Package):
    """Yorick is an interpreted programming language for scientific simulations
       or calculations, postprocessing or steering large simulation codes,
       interactive scientific graphics, and reading, writing, or translating 
       files of numbers. Yorick includes an interactive graphics package, and a
       binary file package capable of translating to and from the raw numeric
       formats of all modern computers. Yorick is written in ANSI C and runs on
       most operating systems (\*nix systems, MacOS X, Windows).
    """

    homepage = "http://dhmunro.github.io/yorick-doc/"
    url =  "https://github.com/dhmunro/yorick/archive/y_2_2_04.tar.gz"

    version('2.2.04', md5='1b5b0da6ad81b2d9dba64d991ec17939')
    version('master', branch='master',
            git='https://github.com/dhmunro/yorick.git')
    version('f90-plugin', branch='f90-plugin',
            git='https://github.com/trmwzm/yorick.git')

    variant('X', default=False, description='Enable X11 support')

    depends_on('libx11', when='+X')

    def install(self, spec, prefix):
        os.environ['FORTRAN_LINKAGE'] = '-Df_linkage'

        make("config")

        filter_file(r'^CC.+',
                    'CC={0}'.format(self.compiler.cc),
                    'Make.cfg')
        filter_file(r'^FC.+',
                    'FC={0}'.format(self.compiler.fc),
                    'Make.cfg')
        filter_file(r'^COPT_DEFAULT.+',
                    'COPT_DEFAULT=-O3',
                    'Make.cfg')

        make()
        make("install")

        try:
            os.makedirs(prefix)
        except OSError:
            pass
        os.chdir("relocate")
        for f in glob.glob('*'):
            if os.path.isdir(f):
                shutil.copytree(f, os.path.join(prefix, f))
            else:
                shutil.copy2(f, os.path.join(prefix, f))
