# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aquila(CMakePackage):
    """Aquila is an open source and cross-platform DSP (Digital Signal Processing) library for C++11."""

    homepage = "http://aquila-dsp.org/"
    git = "https://github.com/zsiciarz/aquila.git"

    version("master")


    