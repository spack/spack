# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-tf-keras
#
# You can edit this file again by typing:
#
#     spack edit py-tf-keras
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyTfKeras(PythonPackage):
    """The TF-Keras library is a pure TensorFlow implementation of Keras, based on the legacy tf.keras codebase. Note that the "main" version of Keras is now Keras 3 (formerly Keras Core), which is a multi-backend implementation of Keras, supporting JAX, PyTorch, and TensorFlow. Keras 3 is being developed at keras-team/keras."""

    homepage = "https://github.com/keras-team/tf-keras"
    pypi = "tf_keras/tf_keras-2.16.0.tar.gz"

    maintainers("jonas-eschle")

    license("Apache-2.0", checked_by="jonas-eschle")

    version("2.16.0", sha256="db53891f1ac98197c2acced98cdca8c06ba8255655a6cb7eb95ed49676118280")

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    # depends_on("python@2.X:2.Y,3.Z:", type=("build", "run"))
    # depends_on("py-pip@X.Y:", type="build")
    # depends_on("py-wheel@X.Y:", type="build")

    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    # depends_on("py-setuptools", type="build")
    # depends_on("py-hatchling", type="build")
    # depends_on("py-flit-core", type="build")
    # depends_on("py-poetry-core", type="build")

    # FIXME: Add additional dependencies if required.
    # depends_on("py-foo", type=("build", "run"))

    def config_settings(self, spec, prefix):
        # FIXME: Add configuration settings to be passed to the build backend
        # FIXME: If not needed, delete this function
        settings = {}
        return settings
