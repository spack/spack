# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPlotnine(PythonPackage):
    """plotnine is an implementation of a grammar of graphics in Python, it is
    based on ggplot2. The grammar allows users to compose plots by explicitly
    mapping data to the visual objects that make up the plot."""

    homepage = "https://plotnine.readthedocs.io/en/stable"
    pypi = "plotnine/plotnine-0.8.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.9.0",
        sha256="340ff64601cddb78ccbca9d4a5dd1a7c56d89cd88c0729d065c30bcb1382cb36",
        url="https://pypi.org/packages/6f/c9/009dc392e404fbe1ae929c631460e11a27d22b53de76dc71b6aa4f34d13b/plotnine-0.9.0-py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="3c938093e20c6e68d1ee4591967a2e5093d185046bad88af00af81bf14215549",
        url="https://pypi.org/packages/e1/cf/e895bd6aea6c12b97fb9e014657aaa8a886b9fd6fc1eb3e90f9f55ddf71a/plotnine-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="f078cd5d76bff885d43be4381e042510ce75a0d202f0071d7230057e15a8f906",
        url="https://pypi.org/packages/a9/37/d8b7ca612ce3d16fe542ebb276238befc2b0b0ba97c31c7c839333c7e33f/plotnine-0.7.1-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="5d87d6e3e8fa71cadceacf74b0306261468a4f1e72a0a3fcfa6cbd49e0d5ddca",
        url="https://pypi.org/packages/aa/ee/9f343ef0719541e02950384978722ea84cc433264cece09a11a0cccb2bf9/plotnine-0.7.0-py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="c271d08edf276f6be09951a4544a1116fc7aa6bc68cadef1b05e29c26ff5f683",
        url="https://pypi.org/packages/19/da/4d2f68e7436e76a3c26ccd804e1bfc5c58fca7a6cba06c71bab68b25e825/plotnine-0.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.9:0.12")
        depends_on("py-descartes@1.1:", when="@0.4:0.8")
        depends_on("py-matplotlib@3.5.0:", when="@0.9:0.10")
        depends_on("py-matplotlib@3.1.1:", when="@0.6:0.8")
        depends_on("py-mizani@0.7.3:", when="@0.8:0.9")
        depends_on("py-mizani@0.7.1:", when="@0.7")
        depends_on("py-mizani@0.6:", when="@0.6")
        depends_on("py-numpy@1.19.0:", when="@0.8:0.10")
        depends_on("py-numpy@1.16.0:", when="@0.6:0.7")
        depends_on("py-pandas@1.3.5:", when="@0.9:0.10")
        depends_on("py-pandas@1.1.0:", when="@0.7.1:0.8")
        depends_on("py-pandas@1.0.3:", when="@0.7:0.7.0")
        depends_on("py-pandas@0.25.0:", when="@0.6")
        depends_on("py-patsy@0.5.1:", when="@0.7:0.12")
        depends_on("py-patsy@0.4.1:", when="@0.2:0.6")
        depends_on("py-scipy@1.5.0:", when="@0.8:0.12")
        depends_on("py-scipy@1.2.0:", when="@0.6:0.7")
        depends_on("py-statsmodels@0.13.2:", when="@0.9:0.10")
        depends_on("py-statsmodels@0.12.1:", when="@0.8")
        depends_on("py-statsmodels@0.11.1:", when="@0.7")
        depends_on("py-statsmodels@0.9.0:", when="@0.6")
