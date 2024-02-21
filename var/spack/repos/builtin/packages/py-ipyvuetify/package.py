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
    pypi = "ipyvuetify/ipyvuetify-1.8.10.tar.gz"

    license("MIT")

    maintainers("jeremyfix")

    version("1.8.10", sha256="9ba44279479f33f5cb83af406aa813050ee96201955c2cba087fd23a843d5b4e")

    depends_on("py-setuptools", type="build")

    depends_on("py-jupyter-packaging", type=("build", "run"))
    depends_on("py-jupyterlab", type=("build", "run"))
    depends_on("py-pynpm", type=("build", "run"))
