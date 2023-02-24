# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVowpalwabbit(PythonPackage):
    """Vowpal Wabbit is a machine learning system which pushes the frontier of
    machine learning with techniques such as online, hashing, allreduce, reductions,
    learning2search, active, and interactive learning. """

    homepage = "https://vowpalwabbit.org/"
    pypi = "vowpalwabbit/vowpalwabbit-9.7.0.tar.gz"

    version("9.7.0", sha256="3b75a71b7250ec210730f613984f698274bc619b3bd7b3fac012819d722fbc52")

    depends_on("py-setuptools", type="build")

    depends_on("boost+program_options+system+thread+math+python+test")
    depends_on("cmake", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn@0.17.1:", type=("build", "run"))
    depends_on("zlib")
