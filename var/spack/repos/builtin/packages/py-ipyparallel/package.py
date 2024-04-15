# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpyparallel(PythonPackage):
    """IPython's architecture for parallel and distributed computing."""

    homepage = "https://github.com/ipython/ipyparallel"
    pypi = "ipyparallel/ipyparallel-7.1.0.tar.gz"

    version(
        "8.4.1",
        sha256="ecce5fc3c2717cc94ed7593eaf95419fb528f7f70abff3c7038f70a33fea1e6b",
        url="https://pypi.org/packages/e2/80/7f01a9a4fd4c3e1d2addd7696335cc07c5b990a11c579f44b417cf316ca4/ipyparallel-8.4.1-py3-none-any.whl",
    )
    version(
        "8.0.0",
        sha256="3365f8020baa2a675b5c7e42b6fe1c03b20e95de7af3330fa5557265ac07451a",
        url="https://pypi.org/packages/62/e6/2aaddc081158cd6bedeed86047ed4609b38fcd0e44ddf0fe002bd8f9f7a6/ipyparallel-8.0.0-py3-none-any.whl",
    )
    version(
        "7.1.0",
        sha256="d72496c1e75e6d26636117b33d3770b66d46b99c2421412676656ca957933ee3",
        url="https://pypi.org/packages/8d/c5/39e862edc26bbaf6973575c20a243705788156d3b1a5657a16eb565ebe54/ipyparallel-7.1.0-py3-none-any.whl",
    )
    version(
        "6.3.0",
        sha256="61013af22cbcbefcaa9ba7b118a6ea1538491a82ef95b0adfd157924777c1df9",
        url="https://pypi.org/packages/3b/e9/03a9189eb39276396309faf28bf833b4328befe4513bbf375b811a36a076/ipyparallel-6.3.0-py3-none-any.whl",
    )
    version(
        "6.2.5",
        sha256="4d11a85c420bfc15bfba74190513227d52b38263a8b2855e0e0eacc6cea27c68",
        url="https://pypi.org/packages/d5/45/abc77804b90034c75f4798df90833d9b61df8928d2358559471fddbfd413/ipyparallel-6.2.5-py2.py3-none-any.whl",
    )
    version(
        "6.2.4",
        sha256="2acbffcbd6da955b47ec7befb320dcad1788cc146cfc7abfa6d1c74436d74d38",
        url="https://pypi.org/packages/3f/82/aaa7a357845a98d4028f27c799f0d3bb2fe55fc1247c73dc712b4ae2344c/ipyparallel-6.2.4-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@8.3:8.6")
        depends_on("py-decorator")
        depends_on("py-entrypoints", when="@7.0.0-beta1:")
        depends_on("py-ipykernel@4.4:", when="@6.2.3:")
        depends_on("py-ipython@4.0.0:")
        depends_on("py-ipython-genutils", when="@:7.0.0-beta2")
        depends_on("py-jupyter-client")
        depends_on("py-psutil", when="@7.0.0-alpha4:")
        depends_on("py-python-dateutil@2:", when="@6:")
        depends_on("py-pyzmq@18:", when="@7.0.0-alpha3:")
        depends_on("py-pyzmq@13:", when="@:7.0.0-alpha1")
        depends_on("py-tornado@5.1:", when="@7:")
        depends_on("py-tornado@4:", when="@:6")
        depends_on("py-tqdm", when="@7.0.0-alpha3:")
        depends_on("py-traitlets@4.3.0:", when="@6.1:")
