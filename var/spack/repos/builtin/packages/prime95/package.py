# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prime95(AutotoolsPackage):
    """
    Prime95, also distributed as the command-line utility mprime for FreeBSD
    and Linux, is a freeware application. 

    Prime95 is a CPU stress testing program. It tests your computer for
    stability issues by stressing your CPU to its maximum limit. 
    Prime95 runs indefinitely and only terminates a stress test when it
    encounters an error and informs the user that the system may be unstable.
    """

    homepage = "https://www.mersenne.org/"
    url = "https://www.mersenne.org/ftp_root/gimps/p95v308b17.linux64.tar.gz"
    maintainers = ["saqibkh"]

    version("30.8b17", sha256="5180c3843d2b5a7c7de4aa5393c13171b0e0709e377c01ca44154608f498bec7")
