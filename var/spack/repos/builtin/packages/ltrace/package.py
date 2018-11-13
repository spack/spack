# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ltrace(AutotoolsPackage):
    """Ltrace intercepts and records dynamic library calls which are called
    by an executed process and the signals received by that process. It
    can also intercept and print the system calls executed by the program."""

    homepage = "https://www.ltrace.org"
    url      = "https://www.ltrace.org/ltrace_0.7.3.orig.tar.bz2"

    version('0.7.3', 'b3dd199af8f18637f7d4ef97fdfb9d14')

    conflicts('platform=darwin', msg='ltrace runs only on Linux.')
