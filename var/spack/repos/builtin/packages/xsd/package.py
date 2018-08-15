##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class Xsd(MakefilePackage):
    """CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema
    to C++ data binding compiler. It support in-memory and event-driven XML
    processing models and is available for a wide range of C++ compilers
    and platforms."""

    homepage = "https://www.codesynthesis.com"
    url      = "https://www.codesynthesis.com/download/xsd/4.0/xsd-4.0.0+dep.tar.bz2"

    version('4.0.0', 'ad3de699eb140e747a0a214462d95fc81a21b494')

    depends_on('xerces-c')
    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make('install', 'install_prefix=' + prefix)

    def setup_environment(self, spack_env, run_env):
        xercesc_lib_flags = self.spec['xerces-c'].libs.search_flags
        spack_env.append_flags('LDFLAGS', xercesc_lib_flags)

    def url_for_version(self, version):
        url = "https://www.codesynthesis.com/download/xsd/{0}/xsd-{1}+dep.tar.bz2"
        return url.format(version.up_to(2), version)
