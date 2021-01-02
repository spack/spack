# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Externalprereq(Package):
    homepage = "http://somewhere.com"
    url      = "http://somewhere.com/prereq-1.0.tar.gz"

    version('1.4', 'f1234567890abcdef1234567890abcde')
