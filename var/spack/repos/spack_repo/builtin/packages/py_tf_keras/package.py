# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTfKeras(PythonPackage):
    """The TF-Keras library is a pure TensorFlow implementation of Keras,
    based on the legacy tf.keras codebase. Note that the "main" version
    of Keras is now Keras 3 (formerly Keras Core), which is a
    multi-backend implementation of Keras, supporting JAX, PyTorch, and TensorFlow.
     Keras 3 is being developed at keras-team/keras."""

    homepage = "https://github.com/keras-team/tf-keras"
    pypi = "tf-keras/tf_keras-2.18.0.tar.gz"
    # url = "https://github.com/keras-team/tf-keras/archive/refs/tags/v2.18.0.tar.gz"

    maintainers("jonas-eschle")

    license("Apache-2.0", checked_by="jonas-eschle")

    max_minor = 18
    # needs TF 2.19: https://github.com/spack/spack/pull/49440
    # version("2.19.0", sha256="b09a407d87a4571ce1e8ca985cfc68483e3d63b2518a5d79a97ad92cb64dbe9c")
    version("2.18.0", sha256="ebf744519b322afead33086a2aba872245473294affd40973694f3eb7c7ad77d")

    # Supported Python versions listed in multiple places:
    # * tf-keras/tools/pip_package/setup.py
    # * CONTRIBUTING.md
    # * PKG-INFO
    depends_on("python@3.9:", type=("build", "run"), when="@2.17:")
    depends_on("py-setuptools", type="build")

    # Required dependencies listed in multiple places:
    # * BUILD
    # * WORKSPACE
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pydot", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    depends_on("protobuf@3.20.3", type="build", when="@2.18:")
    # TODO: uncomment for 2.19
    # depends_on("protobuf@4.23.0", type="build", when="@2.19:")
    # the tf-keras versions are following along with TF versions
    # as defined in oss_setup.py
    for minor_ver in range(18, max_minor + 1):
        depends_on(f"py-tensorflow@2.{minor_ver}", type=("build", "run"), when=f"@2.{minor_ver}")
        # depends_on(f"py-tensorboard@2.{minor_ver}",
        # type=("build", "run"), when=f"@2.{minor_ver}")
    depends_on("py-portpicker", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-numpy@1.26.0:2.0", type=("build", "run"), when="@2.18:")

    depends_on("py-six", type=("build", "run"))
    depends_on("py-absl-py", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
