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


class Turbovnc(CMakePackage):
    """TurboVNC is a derivative of VNC (Virtual Network Computing) 
 that is tuned to provide peak performance for 3D and video workloads.
 TurboVNC was originally a fork of TightVNC 1.3.x, on the surface, 
 the X server and Windows viewer still behave similarly to their parents."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.turbovnc.org/"
    url      = "http://downloads.sourceforge.net/project/turbovnc/2.0.1/turbovnc-2.0.1.tar.gz"


    version('2.1', '6748bb13647d318f0c932394f8298d10')
    version('2.0.1', 'a279fdb9ac86a1ebe82f85ab68353dcc')


    # FIXME: Add dependencies if this package requires them.
    variant('java', default=False, description='Enable Java build')

   
    depends_on('cmake', type='build')
    depends_on("libjpeg-turbo")
    depends_on("libjpeg-turbo+java", when='+java')
    depends_on('jdk', when='+java')
    depends_on("openssl")
    depends_on("pam")
    depends_on("libx11")
    depends_on("libxext")
    depends_on("libxdmcp")
    depends_on("libxau")
    depends_on("libxdamage")
    depends_on("libxcursor")
    depends_on('libxkbfile')
    depends_on('xkeyboard-config')
    depends_on('xkbcomp', type="run")
    depends_on('xkbdata', type='build')

    #def url_for_version(self, version):
        #"""Handle TurboVNC's version-based custom URLs."""
        #return 'http://downloads.sourceforge.net/project/turbovnc/%s/turbovnc-%s.tar.gz' % (
            #version, version)



    def validate(self):
        """
        Checks if incompatible versions of openssl were specified

        :param spec: spec of the package
        :raises RuntimeError: in case of inconsistencies
        """
        spec=self.spec
        if spec.satisfies('@:2.1') and spec.satisfies('^openssl@1.1:'):
            msg = 'turbovnc does not compile with openssl 1.1 '
            raise RuntimeError(msg)

    def cmake_args(self):

        #self.validate()
        options = []
        if '+java' in self.spec:            
            options.append('-DTVNC_BUILDJAVA:BOOL=ON')
        else:
            options.append('-DTVNC_BUILDJAVA:BOOL=OFF')
            options.append('-DTVNC_BUILDNATIVE:BOOL=ON')
            options.append('-DXKB_BASE_DIRECTORY:PATH='+self.spec['xkbdata'].prefix+'/share/X11/xkb')
        if '+debug' in self.spec:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Debug')
        else:
            options.append('-DCMAKE_BUILD_TYPE:STRING=Release')

        return options
    #def install(self, spec, prefix):
        
        #self.validate(spec)

        #def feature_to_bool(feature, on='ON', off='OFF'):
            #if feature in spec:
                #return on
            #return off
##        layout = YamlDirectoryLayout(self.tmpdir)
##        rel_path=layout.relative_path_for_spec(spec)
        #feature_args = []
        ## FIXME: Modify the configure line to suit your build system here.
        #if '+java' not in spec:
            #feature_args.append(
                #'-DTVNC_BUILDJAVA=%s' % feature_to_bool('+java'))
            #feature_args.append(
                #' %s' % feature_to_bool('+java'))
        #feature_args.append('-DCMAKE_VERBOSE_MAKEFILE=ON')
        #feature_args.extend(std_cmake_args)
        #cmake('.', *feature_args)

        ## FIXME: Add logic to build and install here
        #make()
        #make("install")
