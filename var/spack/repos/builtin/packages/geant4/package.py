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


class Geant4(Package):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url      = "http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz"

    version('10.02.p01', 'b81f7082a15f6a34b720b6f15c6289cfe4ddbbbdcef0dc52719f71fac95f7f1c')
    version('10.01.p03', '4fb4175cc0dabcd517443fbdccd97439')

    variant('qt', default=False, description='Enable Qt support')

    depends_on('cmake@3.5:', type='build')

    depends_on("clhep@2.3.1.1~cxx11+cxx14", when="@10.02.p01")
    depends_on("clhep@2.2.0.4~cxx11+cxx14", when="@10.01.p03")
    depends_on("expat")
    depends_on("zlib")
    depends_on("xerces-c")
    depends_on("qt@4.8:", when="+qt")

    def install(self, spec, prefix):
        cmake_args = list(std_cmake_args)
        cmake_args.append('-DXERCESC_ROOT_DIR:STRING=%s' %
                          spec['xerces-c'].prefix)
        cmake_args.append('-DGEANT4_BUILD_CXXSTD=c++14')

        cmake_args += ['-DGEANT4_USE_GDML=ON',
                       '-DGEANT4_USE_SYSTEM_EXPAT=ON',
                       '-DGEANT4_USE_SYSTEM_ZLIB=ON',
                       '-DGEANT4_USE_SYSTEM_CLHEP=ON']

        # fixme: turn off data for now and maybe each data set should
        # go into a separate package to cut down on disk usage between
        # different code versions using the same data versions.
        cmake_args.append('-DGEANT4_INSTALL_DATA=OFF')

        # http://geant4.web.cern.ch/geant4/UserDocumentation/UsersGuides/InstallationGuide/html/ch02s03.html
        # fixme: likely things that need addressing:
        # -DGEANT4_USE_OPENGL_X11=ON

        if '+qt' in spec:
            cmake_args.append('-DGEANT4_USE_QT=ON')

        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path

        with working_dir(build_directory, create=True):
            cmake(source_directory, *cmake_args)
            make()
            make("install")

    def url_for_version(self, version):
        """Handle Geant4's unusual version string."""
        return "http://geant4.cern.ch/support/source/geant4.%s.tar.gz" % version
