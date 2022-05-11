# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyTokenizeRt(PythonPackage):
    """A wrapper around the stdlib `tokenize` which roundtrips."""

    homepage = "https://github.com/asottile/tokenize-rt"
    pypi     = "tokenize_rt/tokenize_rt-4.2.1.tar.gz"

    version('4.2.1', sha256='0d4f69026fed520f8a1e0103aa36c406ef4661417f20ca643f913e33531b3b94')

    depends_on('python@3.6.1:', type=('build', 'run'))
