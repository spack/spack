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


class Genders(AutotoolsPackage):
    """Genders is a static cluster configuration database used for cluster
       configuration management. It is used by a variety of tools and scripts
       for management of large clusters."""

    homepage = "https://github.com/chaos/genders"
    url      = "https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz"

    version('1.22', '9ea59a024dcbddb85b0ed25ddca9bc8e',
            url='https://github.com/chaos/genders/releases/download/genders-1-22-1/genders-1.22.tar.gz')

    variant('perl',   default=False, description='Enable Perl extensions build')
    variant('python', default=False, description='Enable Python extensions build')
    variant('cxx',    default=True,  description='Enable C++ extensions build')
    variant('java',   default=False, description='Enable Java extensions build')

    extends('perl',   when='+perl')
    extends('python', when='+python', type=('build', 'link', 'run'))
    depends_on('jdk', when='+java')

    # FIXME: Known build problems when building Java extensions
    # src/Gendersjni.c:8:10: fatal error: genders.h: No such file or directory

    def configure_args(self):
        spec = self.spec

        args = []

        if '+perl' in spec:
            args.append('--with-perl-extensions')
        else:
            args.append('--without-perl-extensions')

        if '+python' in spec:
            args.append('--with-python-extensions')
        else:
            args.append('--without-python-extensions')

        if '+cxx' in spec:
            args.append('--with-cplusplus-extensions')
        else:
            args.append('--without-cplusplus-extensions')

        if '+java' in spec:
            args.extend([
                '--with-java-extensions',
                'CPPFLAGS=-I{0}'.format(join_path(
                    spec['jdk'].prefix.include, 'linux')),
            ])
        else:
            args.append('--without-java-extensions')

        return args
