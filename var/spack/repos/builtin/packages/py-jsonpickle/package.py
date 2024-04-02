# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsonpickle(PythonPackage):
    """Python library for serializing any arbitrary object graph into JSON."""

    homepage = "https://github.com/jsonpickle/jsonpickle"
    pypi = "jsonpickle/jsonpickle-1.4.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.2.0",
        sha256="de7f2613818aa4f234138ca11243d6359ff83ae528b2185efdd474f62bcf9ae1",
        url="https://pypi.org/packages/c6/85/b4920d8087ef480eed4e7b6b0d46c90674e923e59b22e7929fd17aba5030/jsonpickle-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="c1010994c1fbda87a48f8a56698605b598cb0fc6bb7e7927559fc1100e69aeac",
        url="https://pypi.org/packages/bb/1a/f2db026d4d682303793559f1c2bb425ba3ec0d6fd7ac63397790443f2461/jsonpickle-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="8919c166bac0574e3d74425c7559434062002d9dfc0ac2afa6dc746ba4a19439",
        url="https://pypi.org/packages/af/ca/4fee219cc4113a5635e348ad951cf8a2e47fed2e3342312493f5b73d0007/jsonpickle-1.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-importlib-metadata", when="@1.4.2: ^python@:3.7")
        depends_on("py-importlib-metadata", when="@1.4:1.4.1")
