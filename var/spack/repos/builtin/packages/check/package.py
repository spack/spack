# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Check(AutotoolsPackage):
    """Check is a unit testing framework for C. It features a simple interface
    for defining unit tests, putting little in the way of the developer. Tests
    are run in a separate address space, so both assertion failures and code
    errors that cause segmentation faults or other signals can be caught. Test
    results are reportable in the following: Subunit, TAP, XML, and a generic
    logging format."""

    homepage = "https://libcheck.github.io/check/index.html"
    url      = "https://downloads.sourceforge.net/project/check/check/0.10.0/check-0.10.0.tar.gz"

    version('0.10.0', sha256='f5f50766aa6f8fe5a2df752666ca01a950add45079aa06416b83765b1cf71052')
