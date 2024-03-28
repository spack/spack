# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://github.com/BlueBrain/BluePyEModel"
    pypi = "bluepyemodel/bluepyemodel-0.0.46.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.64",
        sha256="af0a66cefaba9e99b57801a559004821da649e9d6234fff45732445f19da6f97",
        url="https://pypi.org/packages/d1/aa/3924d6aa0dc282ed599ce5f3fef2da264bdcfcdb594cb6f2f418830bcb62/bluepyemodel-0.0.64-py3-none-any.whl",
    )
    version(
        "0.0.59",
        sha256="e587acab723ceaa4ef8d085a93b6495c06519f979d6f63be56acd02e234af199",
        url="https://pypi.org/packages/3f/8f/d0d3df827abec72f66a61d2ffbab9f7e9cfd0c5cc450e8e1b81156a5b24d/bluepyemodel-0.0.59-py3-none-any.whl",
    )
    version(
        "0.0.58",
        sha256="8c1676e239b39a4bad18e4fa6cad340c1c5ce66b8413b11e1e6f81ec707329c5",
        url="https://pypi.org/packages/2d/2f/14fea76becd5c70ca999886fdcb557aa4f28382e6684b49fa9aa527b39c0/bluepyemodel-0.0.58-py3-none-any.whl",
    )
    version(
        "0.0.57",
        sha256="67de314a37f2e2336c8c8b5e6d8656e68a60345eb4bcab96f66c5e5b25f260d7",
        url="https://pypi.org/packages/fd/56/1b7ae8e37ffc70a732886db87b702a8109a06022229df676c44d51dfd742/bluepyemodel-0.0.57-py3-none-any.whl",
    )
    version(
        "0.0.46",
        sha256="01adf7b5b0dc867faa0d0f3874a1d83d493e07fddc4cfd8ea45b379f30896bc3",
        url="https://pypi.org/packages/f5/c4/ac4bcb42c16f3f737fb2e3d27ed66dfdb727ae7dfa0921f5d880ef646728/bluepyemodel-0.0.46-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bluepyefe@2.2:")
        depends_on("py-bluepyopt@1.12.12:", when="@:0.0.76")
        depends_on("py-configparser")
        depends_on("py-currentscape@1:")
        depends_on("py-efel@3.1:")
        depends_on("py-fasteners@0.16:")
        depends_on("py-gitpython")
        depends_on("py-ipyparallel@6.3:")
        depends_on("py-jinja2@3.0.3:3.0", when="@:0.0.71")
        depends_on("py-morph-tool@2.8:")
        depends_on("py-neurom@3:")
        depends_on("py-neuron@8.0.0:")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-pyyaml")
        depends_on("py-scipy")
        depends_on("py-tqdm")
