# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvuetify(PythonPackage):
    """
    Jupyter widgets based on vuetify UI components which implement Google's
    Material Design Spec with the Vue.js framework.
    """

    homepage = "https://github.com/widgetti/ipyvuetify/tree/master"
    pypi = "ipyvuetify/ipyvuetify-1.9.0.tar.gz"

    license("MIT")

    maintainers("jeremyfix")

    version(
        "1.9.0",
        sha256="a190f62a10e89e92a0e25641c84c739e31f66680858d987b8a180b24e2278dec",
        url="https://pypi.org/packages/d9/15/b3b6560dd4984660a75aff9cdf3e7d574b3b3fecb81fb6affa138d6c760b/ipyvuetify-1.9.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-ipyvue@1.7:1", when="@1.8.8:1")
