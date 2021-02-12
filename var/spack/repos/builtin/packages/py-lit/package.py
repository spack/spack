# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLit(PythonPackage):
    """lit is a portable tool for executing LLVM and Clang style test suites,
       summarizing their results, and providing indication of failures. lit is
       designed to be a lightweight testing tool with as simple a user
       interface as possible."""

    pypi = "lit/lit-0.5.0.tar.gz"

    version('0.11.1', sha256='2b15be8a84b691d9473911e7a73100e8ba3abef4965920ef6ac65a7d75dc3936')
    version('0.11.0', sha256='a723e348a7ee898e9832bde2374412e08e926c80bdb61e2a6979024d493b3eda')
    version('0.10.1', sha256='b81c770a3a27d9faaf9d7cefb4905f3a193e3bb30265b49c5de25e793a326a77')
    version('0.10.0', sha256='196d2862e6f4ec4339d908a7419bbd290afcca61bef543a07504092774da488f')
    version('0.9.0',  sha256='c035aa0a233633f7046745164a153a57d8bbcaf9b833232438cf4d2923d8786e')
    version('0.8.0',  sha256='ec443e53256756cbcd0023b8bf10e6d4308c28f31cb23304bb408db9030f9d53')
    version('0.7.1',  sha256='ecef2833aef7f411cb923dac109c7c9dcc7dbe7cafce0650c1e8d19c243d955f')
    version('0.5.0',  sha256='3ea4251e78ebeb2e07be2feb33243d1f8931d956efc96ccc2b0846ced212b58c')

    depends_on('py-setuptools', type='build')
