# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class UnconstrainableConflict(Package):
    """Package with a conflict whose trigger cannot constrain its constraint."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/unconstrainable-conflict-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    # Two conflicts so there's always one that is not the current platform
    conflicts('target=x86_64', when='platform=darwin')
    conflicts('target=aarch64', when='platform=linux')
