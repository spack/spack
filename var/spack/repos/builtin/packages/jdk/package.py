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
#------------------------------------------------------------------------------
# Author: Justin Too <too1@llnl.gov>
#------------------------------------------------------------------------------
import distutils
from distutils import dir_util
from subprocess import call

import spack
from spack import *
import llnl.util.tty as tty

class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation
       in the form of a binary product aimed at Java developers."""
    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    version('8u66-linux-x64', '88f31f3d642c3287134297b8c10e61bf',
        url="http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz")

    # Oracle requires that you accept their License Agreement in order
    # to access the Java packages in download.oracle.com. In order to
    # automate this process, we need to utilize these additional curl
    # commandline options.
    #
    # See http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux
    curl_options=[
        '-j', # junk cookies
        '-H', # specify required License Agreement cookie
        'Cookie: oraclelicense=accept-securebackup-cookie']

    def do_fetch(self, mirror_only=False):
        # Add our custom curl commandline options
        tty.msg(
            "[Jdk] Adding required commandline options to curl " +
            "before performing fetch: %s" %
            (self.curl_options))

        for option in self.curl_options:
            spack.curl.add_default_arg(option)

        # Now perform the actual fetch
        super(Jdk, self).do_fetch(mirror_only)


    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix)
