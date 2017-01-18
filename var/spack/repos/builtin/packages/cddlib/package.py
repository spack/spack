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


class Cddlib(AutotoolsPackage):
    """The C-library cddlib is a C implementation of the Double Description
    Method of Motzkin et al. for generating all vertices (i.e. extreme points)
    and extreme rays of a general convex polyhedron in R^d given by a system
    of linear inequalities"""
    homepage = "https://www.inf.ethz.ch/personal/fukudak/cdd_home/"
    # This is the original download url. It is currently down [2016-08-23],
    # but should be reinstated or updated once the issue is resolved.
    # url = "ftp://ftp.ifor.math.ethz.ch/pub/fukuda/cdd/cddlib-094h.tar.gz"
    url = "http://pkgs.fedoraproject.org/lookaside/pkgs/cddlib/cddlib-094h.tar.gz/1467d270860bbcb26d3ebae424690e7c/cddlib-094h.tar.gz"

    def url_for_version(self, version):
        # Since the commit id is part of the version, we can't
        # auto-generate the string, and we need to explicitly list all
        # known versions here. Currently, there is only one version.
        if str(version) == '0.94h':
            return "http://pkgs.fedoraproject.org/lookaside/pkgs/cddlib/cddlib-094h.tar.gz/1467d270860bbcb26d3ebae424690e7c/cddlib-094h.tar.gz"
        raise InstallError("Unsupported version %s" % str(version))

    version('0.94h', '1467d270860bbcb26d3ebae424690e7c')

    # Note: It should be possible to build cddlib also without gmp

    depends_on("gmp")
    depends_on("libtool", type="build")
