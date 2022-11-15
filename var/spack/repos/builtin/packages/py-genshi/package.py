# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGenshi(PythonPackage):
    """Python toolkit for generation of output for the web"""

    pypi = "Genshi/Genshi-0.7.7.tar.gz"

    version("0.7.7", sha256="c100520862cd69085d10ee1a87e91289e7f59f6b3d9bd622bf58b2804e6b9aab")
    version("0.7", sha256="1d154402e68bc444a55bcac101f96cb4e59373100cc7a2da07fbf3e5cc5d7352")
    version("0.6.1", sha256="fed947f11dbcb6792bb7161701ec3b9804055ad68c8af0ab4f0f9b25e9a18dbd")
    version("0.6", sha256="32aaf76a03f88efa04143bf80700399e6d84eead818fdd19d763fd76af972a4b")

    # Unfortunately, upstream's versioning scheme neglected the trailing zero
    # x.x.0 which means that the spec @:0.7 also includes @0.7.7 which in a few
    # cases below is not what we want.  Therefore explicitly use @0.7.0 to deal
    # with this ambiguity.
    #
    # Older version of python before support for Py_UNICODE->str in genshi/_speedup.c
    depends_on("python@:3.2", when="@:0.7.0", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    # setup.py of 0.7 uses setup(features = ...) which was removed in
    # setuptools 46.0.0.
    depends_on("py-setuptools@:45", type="build", when="@:0.7.0")
    depends_on("py-six", type=("build", "run", "test"))

    # Suite of unittests added in 0.6.1.
    @when("@0.6.1:")
    def test(self):
        # All the unittests pass for py-genshi@0.7.7 but 14 tests fail for
        # @0.6.1:0.7, many of them related to templates, likely because the
        # template path needs to be setup.  But those versions didn't use tox
        # and setting up the test environment to find the template files doesn't
        # seem to be documented.
        python("-m", "unittest", "-v", "genshi.tests.suite")
