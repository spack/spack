# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumexpr(PythonPackage):
    """Fast numerical expression evaluator for NumPy"""

    homepage = "https://github.com/pydata/numexpr"
    url = "https://github.com/pydata/numexpr/archive/v2.7.0.tar.gz"

    version("2.8.4", sha256="0e21addd25db5f62d60d97e4380339d9c1fb2de72c88b070c279776ee6455d10")
    version("2.8.3", sha256="389ceefca74eff30ec3fd03fc4c3b7ab3df8f22d1f235117a392ce702ed208c0")
    version("2.7.3", sha256="00d6b1518605afe0ed10417e0ff07123e5d531c02496c6eed7dd4b9923238e1e")
    version("2.7.2", sha256="7d1b3790103221feda07f4a93a4fa5c6654f46865197a677ca6f27eb5cb4e5ef")
    version("2.7.0", sha256="1923f038b90cc69635871968ed742be7775c879451c612f173c2547c823c9561")
    version("2.6.9", sha256="d57267bbdf10906f5ed7841b3484bec4af0494102b50e89ba316924cc7a7fd46")
    version("2.6.5", sha256="fe78a78e002806e87e012b6105f3b3d52d47fc7a72bafb56341fcec7ce02cfd7")
    version("2.6.1", sha256="e92c83d066fa8da63864d69b5f218287cc31437ae844db77390f2183123aab22")
    version("2.5", sha256="4ca111a9a27c9513c2e2f5b70c0a84ea69081d7d8e4512d4c3f26a485292de0d")
    version("2.4.6", sha256="2681faf55a3f19ba4424cc3d6f0a10610ebd49f029f8453f0ba64dd5c0fe4e0f")

    depends_on("python@3.7:", when="@2.8.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy@1.13.3:", type=("build", "run"), when="@2.8.3:")
    # https://github.com/pydata/numexpr/issues/397
    depends_on("py-numpy@1.7:1.22", type=("build", "run"), when="@:2.7")

    # Historical dependencies
    depends_on("py-packaging", type=("build", "run"), when="@2.8.3")
