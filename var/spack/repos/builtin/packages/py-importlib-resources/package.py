# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibResources(PythonPackage):
    """Read resources from Python packages"""

    homepage = "https://github.com/python/importlib_resources"
    pypi = "importlib_resources/importlib_resources-1.0.2.tar.gz"

    license("Apache-2.0")

    version(
        "5.12.0",
        sha256="7b1deeebbf351c7578e09bf2f63fa2ce8b5ffec296e0d349139d43cca061a81a",
        url="https://pypi.org/packages/38/71/c13ea695a4393639830bf96baea956538ba7a9d06fcce7cef10bfff20f72/importlib_resources-5.12.0-py3-none-any.whl",
    )
    version(
        "5.9.0",
        sha256="f78a8df21a79bcc30cfd400bdc38f314333de7c0fb619763f6b9dabab8268bb7",
        url="https://pypi.org/packages/d3/91/4df247dd4da18b72b5bbabe1fa2b85029c34e1d6f0afdd6329d15d6bf2b5/importlib_resources-5.9.0-py3-none-any.whl",
    )
    version(
        "5.3.0",
        sha256="7a65eb0d8ee98eedab76e6deb51195c67f8e575959f6356a6e15fd7e1148f2a3",
        url="https://pypi.org/packages/b1/8e/f29e92e403acda0e28789c0f994500239dff45065c3b28e3a2855afc4f9a/importlib_resources-5.3.0-py3-none-any.whl",
    )
    version(
        "5.2.3",
        sha256="ae35ed1cfe8c0d6c1a53ecd168167f01fa93b893d51a62cdf23aea044c67211b",
        url="https://pypi.org/packages/11/8e/84a6a778a1160cefcef1192a7bd26e4e6689981553aff13c2b2b6f1c352f/importlib_resources-5.2.3-py3-none-any.whl",
    )
    version(
        "5.2.2",
        sha256="2480d8e07d1890056cb53c96e3de44fead9c62f2ba949b0f2e4c4345f4afa977",
        url="https://pypi.org/packages/f2/6c/2f3b930513bb971172ffceb63cf4e910944e57451724e69b1dec97cfefa6/importlib_resources-5.2.2-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="885b8eae589179f661c909d699a546cf10d83692553e34dca1bf5eb06f7f6217",
        url="https://pypi.org/packages/82/70/7bf5f275a738629a7252c30c8461502d3658a75363db9f4f88ddbeb9eeac/importlib_resources-5.1.0-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="6e2783b2538bd5a14678284a3962b0660c715e5a0f10243fd5e00a4b5974f50b",
        url="https://pypi.org/packages/2f/f7/b4aa02cdd3ee7ebba375969d77c00826aa15c5db84247d23c89522dccbfa/importlib_resources-1.0.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@5.6:5.12")
        depends_on("py-zipp@3.1:", when="@5.1.4: ^python@:3.9")
        depends_on("py-zipp@0.4:", when="@1.1:5.1.3 ^python@:3.7")
