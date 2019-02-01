# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Boostmplcartesianproduct(Package):
    """Cartesian_product is an extension to the Boost.MPL library and as such
       requires a version of the Boost libraries on your system.
    """

    homepage = "http://www.organicvectory.com/index.php?option=com_content&view=article&id=75:boostmplcartesianproduct&catid=42:boost&Itemid=78"
    url      = "https://github.com/quinoacomputing/BoostMPLCartesianProduct/tarball/20161205"

    version('20161205', 'b0c8534ee807484ffd161723cbc8fc04')

    def install(self, spec, prefix):
        install_tree('boost/mpl', join_path(prefix.include, 'boost', 'mpl'))
