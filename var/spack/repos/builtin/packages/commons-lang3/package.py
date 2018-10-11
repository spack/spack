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


class CommonsLang3(Package):
    """The standard Java libraries fail to provide enough methods for
    manipulation of its core classes. Apache Commons Lang provides these
    extra methods.

    Lang provides a host of helper utilities for the java.lang API, notably
    String manipulation methods, basic numerical methods, object reflection,
    concurrency, creation and serialization and System properties. Additionally
    it contains basic enhancements to java.util.Date and a series of utilities
    dedicated to help with building methods, such as hashCode, toString and
    equals."""

    homepage = "http://commons.apache.org/proper/commons-lang/"
    url      = "https://archive.apache.org/dist/commons/lang/binaries/commons-lang3-3.7-bin.tar.gz"

    version('3.7', 'c7577443639dc6efadc80f1cbc7fced5')

    extends('jdk')
    depends_on('java@7:', type='run')

    def install(self, spec, prefix):
        install('commons-lang3-{0}.jar'.format(self.version), prefix)
