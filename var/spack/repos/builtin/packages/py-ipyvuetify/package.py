# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyvuetify(PythonPackage):
    """Jupyter widgets based on vuetify UI components"""

    homepage = "https://github.com/widgetti/ipyvuetify"
    pypi = "ipyvuetify/ipyvuetify-1.8.5.tar.gz"

    version("1.8.5", sha256="c1f88485dcac8324c8e134cf38fcea1fb5f9bd3e75836d055713e354f158f565")

    depends_on("py-setuptools", type="build")
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ipyvue@1.5:2", type=("build", "run"))
