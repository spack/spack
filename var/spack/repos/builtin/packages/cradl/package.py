# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cradl
#
# You can edit this file again by typing:
#
#     spack edit cradl
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Cradl(Package):
    """The CRADL proxy application captured performance metrics during
    inference on data from multiphysics codes, specifically ALE
    hydrodynamics codes."""

    homepage = "https://github.com/LLNL/CRADL"
    url      = "https://github.com/LLNL/CRADL/archive/master.zip"
    git      = "https://github.com/LLNL/CRADL.git"


    version('master', branch='master')

    depends_on('py-pandas')
    depends_on('py-torch')
    depends_on('py-torchvision')
    depends_on('py-apex')
    #pip install GPUtil
    depends_on('py-matplotlib')
    depends_on('py-mpi4py')



    def install(self, spec, prefix):
        # FIXME: Unknown build system
        make()
        make('install')
