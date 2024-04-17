# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchNodejsVersion(PythonPackage):
    """Hatch plugin for versioning from a package.json file."""

    homepage = "https://github.com/agoose77/hatch-nodejs-version"
    pypi = "hatch_nodejs_version/hatch_nodejs_version-0.3.1.tar.gz"

    license("MIT")

    version(
        "0.3.1",
        sha256="4570e00fe75a99075dd51d195352c9d7cc2f6186d4046ce58fd47da3a0583702",
        url="https://pypi.org/packages/f3/5b/a19a9262a2c0079685f43a961b400a280c6db1670c844093145edef902c5/hatch_nodejs_version-0.3.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.2:")
        depends_on("py-hatchling@0.21:", when="@0.2:")
