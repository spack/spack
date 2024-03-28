# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStackData(PythonPackage):
    """Extract data from python stack frames and tracebacks for informative
    displays."""

    homepage = "http://github.com/alexmojaki/stack_data"
    pypi = "stack_data/stack_data-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.6.2",
        sha256="cbb2a53eb64e5785878201a97ed7c7b94883f48b87bfb0bbe8b623c74679e4a8",
        url="https://pypi.org/packages/6a/81/aa96c25c27f78cdc444fec27d80f4c05194c591465e491a1358d8a035bc1/stack_data-0.6.2-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="66d2ebd3d7f29047612ead465b6cae5371006a71f45037c7e2507d01367bce3b",
        url="https://pypi.org/packages/9d/ad/22b5d86e421b2786aeb166cf51d519ce5a2a8878c7542d3e58e75aac02b5/stack_data-0.5.0-py3-none-any.whl",
    )
    version(
        "0.2.0",
        sha256="999762f9c3132308789affa03e9271bbbe947bf78311851f4d485d8402ed858e",
        url="https://pypi.org/packages/6b/25/9a454b432df53ffbbb4f03198c3347f393c34f4de07fb652563bdbdf91e8/stack_data-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-asttokens@2.1:", when="@0.6:")
        depends_on("py-asttokens", when="@0.0.7:0.5")
        depends_on("py-executing@1.2:", when="@0.6:")
        depends_on("py-executing", when="@0.0.7:0.5")
        depends_on("py-pure-eval", when="@0.0.7:")
