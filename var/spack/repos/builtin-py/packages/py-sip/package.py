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
import os


class PySip(Package):
    """SIP is a tool that makes it very easy to create Python bindings for C
       and C++ libraries."""
    homepage = "http://www.riverbankcomputing.com/software/sip/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.5/sip-4.16.5.tar.gz"

    version('4.16.5', '6d01ea966a53e4c7ae5c5e48c40e49e5')
    version('4.16.7', '32abc003980599d33ffd789734de4c36')

    extends('python')

    def install(self, spec, prefix):
        python('configure.py',
               '--destdir=%s' % site_packages_dir,
               '--bindir=%s' % spec.prefix.bin,
               '--incdir=%s' % python_include_dir,
               '--sipdir=%s' % os.path.join(spec.prefix.share, 'sip'))
        make()
        make('install')
