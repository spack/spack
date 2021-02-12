# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlExporterTiny(PerlPackage):
    """An exporter with the features of Sub::Exporter but only core
    dependencies"""

    homepage = "http://search.cpan.org/~tobyink/Exporter-Tiny/lib/Exporter/Tiny.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.000000.tar.gz"

    version('1.002002',  sha256='00f0b95716b18157132c6c118ded8ba31392563d19e490433e9a65382e707101')
    version('1.002001',  sha256='a82c334c02ce4b0f9ea77c67bf77738f76a9b8aa4bae5c7209d1c76453d3c48d')
    version('1.002000',  sha256='4f7f79c6252645b31b74be0ac75836e0d6199970183fdf2a77d66decb0530301')
    version('1.001_001', sha256='4028af291bf39cadffd5aa4e03bb93c1c753b0beb545bba89c5920c6d20ca7fd')
    version('1.001_000', sha256='1370df7805d2fe458347fa1df609ed334aeeb45be0776c31cc6b704773682de0')
    version('1.000000', sha256='ffdd77d57de099e8f64dd942ef12a00a3f4313c2531f342339eeed2d366ad078')
