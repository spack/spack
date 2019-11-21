# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Iperf(AutotoolsPackage):
    """
    Iperf is a network traffic tool for measuring TCP and UDP
    performance.
    The goals include maintaining an active iperf 2 code base
    (code originated from iperf 2.0.5), preserving interoperability
    with iperf 2.0.5 clients and servers, preserving the output
    for scripts (new enhanced output requires -e),adopt known 2.0.x
    bug fixes, maintain broad platform support, as well as add
    some essential feature enhancements mostly driven by WiFi testing needs.
    """

    homepage = "https://sourceforge.net/"
    url      = "https://sourceforge.net/projects/iperf2/files/iperf-2.0.13.tar.gz/download"

    version('2.0.13', sha256='c88adec966096a81136dda91b4bd19c27aae06df4d45a7f547a8e50d723778ad')
