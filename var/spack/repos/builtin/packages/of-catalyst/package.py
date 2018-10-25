##############################################################################
# Copyright (c) 2017 Simone Bna, CINECA.
#
# This file was authored by Simone Bna <simone.bna@cineca.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for the LLNL notice and LGPL.
#
# License
# -------
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
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
from spack import *


class OfCatalyst(CMakePackage):
    """Of-catalyst is a library for OpenFOAM that provides a runtime-selectable
    function object for embedding ParaView Catalyst in-situ visualization
    into arbitrary OpenFOAM simulations.
    Supports in-situ conversion of the following types:
      1) finite volume meshes and fields, single or multi-region;
      2) finite area meshes and fields, single region;
      3) lagrangian (clouds), single or multiple clouds.
    This offering is part of the community repository supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    # Currently only via git
    homepage = "https://develop.openfoam.com/Community/catalyst"
    gitrepo  = "https://develop.openfoam.com/Community/catalyst.git"

    version('1806', git=gitrepo, tag='v1806')
    version('develop', branch='develop', git=gitrepo)

    variant('full', default=False, description='Build against paraview (full) or catalyst (light)')

    depends_on('openfoam-com@1806', when='@1806', type=('build', 'link', 'run'))
    depends_on('openfoam-com@develop', when='@develop', type=('build', 'link', 'run'))
    depends_on('catalyst@5.5:', when='~full')
    depends_on('paraview@5.5:+osmesa~qt', when='+full')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('LD_LIBRARY_PATH', join_path(self.prefix,
                             'lib'))

    @property
    def root_cmakelists_dir(self):
        """The relative path to the directory containing CMakeLists.txt

        This path is relative to the root of the extracted tarball,
        not to the ``build_directory``. Defaults to the current directory.

        :return: directory containing CMakeLists.txt
        """
        return join_path(self.stage.source_path, join_path('src', 'catalyst'))

    def cmake_args(self):
        """Populate cmake arguments for ParaView."""
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY:PATH=%s' % join_path(
                self.stage.source_path,
                'spack-build'),
            '-DCMAKE_INSTALL_PREFIX:PATH=%s' % self.prefix
        ]

        return cmake_args
