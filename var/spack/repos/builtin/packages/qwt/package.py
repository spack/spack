##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class Qwt(Package):
    """The Qwt library contains GUI Components and utility classes which are
    primarily useful for programs with a technical background. Beside a
    framework for 2D plots it provides scales, sliders, dials, compasses,
    thermometers, wheels and knobs to control or display values, arrays, or
    ranges of type double.
    """
    homepage = "http://qwt.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/qwt/qwt/5.2.2/qwt-5.2.2.tar.bz2"

    version('5.2.2', '70d77e4008a6cc86763737f0f24726ca')

    depends_on("qt")

    def install(self, spec, prefix):

        # Subvert hardcoded prefix
        filter_file(r'/usr/local/qwt-\$\$VERSION', prefix, 'qwtconfig.pri')

        qmake = which('qmake')
        qmake()
        make()
        make("install")
