# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpcap(AutotoolsPackage):
    "libpcap is a portable library in C/C++ for packet capture"
    homepage = "http://www.tcpdump.org/"
    list_url = "http://www.tcpdump.org/release/"
    url      = "http://www.tcpdump.org/release/libpcap-1.8.1.tar.gz"

    version('1.8.1', '3d48f9cd171ff12b0efd9134b52f1447')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
