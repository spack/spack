# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
#     spack install gpuscout
#
# You can edit this file again by typing:
#
#     spack edit gpuscout
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Gpuscout(CMakePackage):
    """GPUscout: A tool for discovering data movement-related bottlenecks on NVidia GPUs."""
    
    homepage = "https://github.com/caps-tum/GPUscout"
    url = "https://codeload.github.com/caps-tum/GPUscout/tar.gz/refs/tags/v0.1.0"
    git = "https://github.com/caps-tum/GPUscout.git"

    maintainers('stepanvanecek')

    license("Apache-2.0")

    version('0.2.1', sha256='78db030c443b971358905460c53c514134c18ebca9cafc26bfcfa297ff17683b', extension='tar.gz')
    version('master',  branch='master')

    depends_on('cmake@3.27:', type='build')
    depends_on('cuda@12:')

    def cmake_args(self):
        args = []
        return args

