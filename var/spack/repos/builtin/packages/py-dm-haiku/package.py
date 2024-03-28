# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDmHaiku(PythonPackage):
    """JAX-based neural network library"""

    homepage = "https://github.com/deepmind/dm-haiku"
    pypi = "dm-haiku/dm-haiku-0.0.5.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.12",
        sha256="7448a43a6486bff95253f84e18eacc607d9c1256592573117a9d1d23e2780706",
        url="https://pypi.org/packages/1c/c2/4a32e22bad1c5c675ac53701b099ce39c286970326512d3e9b06f8866f7d/dm_haiku-0.0.12-py3-none-any.whl",
    )
    version(
        "0.0.7",
        sha256="d06a2fededd436837f69c686511eddc9b887b0eaf76a921316289a7d7e9d80e3",
        url="https://pypi.org/packages/4d/81/0d8e5822560045ddf4e723f2f8b1fd4f4c30773ed001b9102b77bf517cbb/dm_haiku-0.0.7-py3-none-any.whl",
    )
    version(
        "0.0.5",
        sha256="e2cb422f476eb686dfba670a1d2257d8c20d2f87006665a79b97e5de50fa8379",
        url="https://pypi.org/packages/ae/5b/38871efe524b74798efb5f49c7daf85fbe30aa316e09a5ed7bd77ca43aff/dm_haiku-0.0.5-py3-none-any.whl",
    )

    variant("jax", default=False)

    with default_args(type="run"):
        depends_on("py-absl-py@0.7.1:")
        depends_on("py-flax@0.7.1:", when="@0.0.11:")
        depends_on("py-jax@0.4.24:", when="@0.0.12:+jax")
        depends_on("py-jax@0.3.5", when="@0.0.7+jax")
        depends_on("py-jax@0.2.22", when="@0.0.5:0.0.5.0+jax")
        depends_on("py-jaxlib@0.4.24:", when="@0.0.12:+jax")
        depends_on("py-jaxlib@0.3.5", when="@0.0.7+jax")
        depends_on("py-jaxlib@0.1.73", when="@0.0.5:0.0.5.0+jax")
        depends_on("py-jmp@0.0.2:", when="@0.0.5:0.0.5.0,0.0.6:")
        depends_on("py-numpy@1.18.0:")
        depends_on("py-tabulate@0.8.9:", when="@0.0.4:")

    # AttributeError: module 'jax' has no attribute 'xla'
    conflicts("^py-jax@0.4.14:", when="@:0.0.7")
