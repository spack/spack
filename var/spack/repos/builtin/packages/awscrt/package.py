# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install awscli-v2
#
# You can edit this file again by typing:
#
#     spack edit awscli-v2
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Awscrt(PythonPackage):
    """Python 3 bindings for the AWS Common Runtime."""

    homepage = "https://docs.aws.amazon.com/sdkref/latest/guide/common-runtime.html"
    pypi = "awscrt/awscrt-0.16.16.tar.gz"

    maintainers("climbfuji")

    version("0.16.16", sha256="13075df2c1d7942fe22327b6483274517ee0f6ae765c4e6b6ae9ef5b4c43a827")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
