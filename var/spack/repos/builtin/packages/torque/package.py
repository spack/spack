# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Torque(BundlePackage):
    """Placeholder package for external TORUQE/PBS installation."""

    homepage = "https://github.com/abarbu/torque"

    version('3.0.4')
    version('3.0.2')

    provides('pbs')
