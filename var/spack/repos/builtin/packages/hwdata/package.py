# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Hwdata(AutotoolsPackage):
    """Hardware identification and configuration data."""

    homepage = "https://github.com/vcrhonek/hwdata"
    url      = "https://github.com/vcrhonek/hwdata/archive/v0.337.tar.gz"

    version('0.340', sha256='e3a0ef18af6795a362345a2c2c7177be351cb27b4cc0ed9278b7409759258802')
