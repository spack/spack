# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpywidgets(PythonPackage):
    """IPython widgets for the Jupyter Notebook"""

    homepage = "https://github.com/ipython/ipywidgets"
    pypi = "ipywidgets/ipywidgets-7.6.5.tar.gz"

    license("BSD-3-Clause")

    version(
        "8.0.2",
        sha256="1dc3dd4ee19ded045ea7c86eb273033d238d8e43f9e7872c52d092683f263891",
        url="https://pypi.org/packages/e4/56/990c10ca8751182ace2464cb0e4baafb7087a40c185c9142b9cd18683fac/ipywidgets-8.0.2-py3-none-any.whl",
    )
    version(
        "7.7.0",
        sha256="e58ff58bc94d481e91ecb6e13a5cb96a87b6b8ade135e055603d0ca24593df38",
        url="https://pypi.org/packages/86/7d/06b48ec5fd605775c7e85b3ea397d8f0294f66d570bcee59496eb5195fc5/ipywidgets-7.7.0-py2.py3-none-any.whl",
    )
    version(
        "7.6.5",
        sha256="d258f582f915c62ea91023299603be095de19afb5ee271698f88327b9fe9bf43",
        url="https://pypi.org/packages/6b/bb/285066ddd710779cb69f03d42fa72fbfe4352b4895eb6abab551eae1535a/ipywidgets-7.6.5-py2.py3-none-any.whl",
    )
    version(
        "7.6.3",
        sha256="e6513cfdaf5878de30f32d57f6dc2474da395a2a2991b94d487406c0ab7f55ca",
        url="https://pypi.org/packages/11/53/084940a83a8158364e630a664a30b03068c25ab75243224d6b488800d43a/ipywidgets-7.6.3-py2.py3-none-any.whl",
    )
    version(
        "7.5.1",
        sha256="13ffeca438e0c0f91ae583dc22f50379b9d6b28390ac7be8b757140e9a771516",
        url="https://pypi.org/packages/56/a0/dbcf5881bb2f51e8db678211907f16ea0a182b232c591a6d6f276985ca95/ipywidgets-7.5.1-py2.py3-none-any.whl",
    )
    version(
        "7.4.2",
        sha256="0f2b5cde9f272cb49d52f3f0889fdd1a7ae1e74f37b48dac35a83152780d2b7b",
        url="https://pypi.org/packages/30/9a/a008c7b1183fac9e52066d80a379b3c64eab535bd9d86cdc29a0b766fd82/ipywidgets-7.4.2-py2.py3-none-any.whl",
    )
    version(
        "5.2.2",
        sha256="44d5ae2c1a86cf9841c125532010e56c69a18727634fffabc1b3846d108029ce",
        url="https://pypi.org/packages/d2/0c/56a7ed25c07b845bd3a9c1843e346ae5874308187b47f4b76ff2eb94d862/ipywidgets-5.2.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@8.0.0-beta1:")
        depends_on("py-ipykernel@4.5.1:", when="@6.0.0:7.7.3,7.7.5:7.7,8:8.0.4,8.0.6:8.0")
        depends_on("py-ipython@6.1:", when="@8:")
        depends_on("py-ipython@4.0.0:", when="@5.2.3:5,6.0.0:7")
        depends_on("py-ipython-genutils@0.2:", when="@7.6.4:7")
        depends_on("py-jupyterlab-widgets@3.0.0:", when="@8.0.0:8.0.5")
        depends_on("py-jupyterlab-widgets@1.0.0:", when="@7.6.0:7.6.5,7.7:7.7.1")
        depends_on("py-nbformat@4.2:", when="@6.0.0:7.7.0,8:8.0.0-rc0")
        depends_on("py-traitlets@4.3.1:", when="@6.0.0:")
        depends_on("py-widgetsnbextension@4.0.0:", when="@8.0.0:8.0.5")
        depends_on("py-widgetsnbextension@3.6.0:3", when="@7.7.0:7.7.4")
        depends_on("py-widgetsnbextension@3.5.0:3.5", when="@7.5.0:7.7.0-alpha0")
        depends_on("py-widgetsnbextension@3.4", when="@7.4")

    # pip silently replaces distutils with setuptools
