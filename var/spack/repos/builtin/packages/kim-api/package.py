# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KimApi(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
       reliable, reproducible, and portable. Computer implementations of
       inter-atomic models are archived in OpenKIM, verified for coding
       integrity, and tested by computing their predictions for a variety
       of material properties. Models conforming to the KIM application
       programming interface (API) work seamlessly with major simulation
       codes that have adopted the KIM API standard.
    """
    homepage = "https://openkim.org/"
    git      = "https://github.com/openkim/kim-api"

    version('develop', branch='master')
    version('2.0rc1', commit="c2ab409ec0154ebd85d20a0a1a0bd2ba6ea95a9c") 

    def cmake_args(self):
        args = ['-DBUILD_MODULES=OFF']

        return args
