# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenshi(PythonPackage):
    """Python toolkit for generation of output for the web"""

    pypi = "Genshi/Genshi-0.7.7.tar.gz"

    version("0.7.7", sha256="c100520862cd69085d10ee1a87e91289e7f59f6b3d9bd622bf58b2804e6b9aab")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run", "test"))

    def test(self):
        # All the unittests pass for py-genshi@0.7.7 but 14 tests fail for
        # @0.6.1:0.7, many of them related to templates, likely because the
        # template path needs to be setup.  But those versions didn't use tox
        # and setting up the test environment to find the template files doesn't
        # seem to be documented.
        python("-m", "unittest", "-v", "genshi.tests.suite")
