# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJaracoClasses(PythonPackage):
    """Utility functions for Python class constructs"""

    homepage = "https://github.com/jaraco/jaraco.classes"
    pypi = "jaraco.classes/jaraco.classes-3.2.2.tar.gz"

    license("MIT")

    version(
        "3.2.3",
        sha256="2353de3288bc6b82120752201c6b1c1a14b058267fa424ed5ce5984e3b922158",
        url="https://pypi.org/packages/60/28/220d3ae0829171c11e50dded4355d17824d60895285631d7eb9dee0ab5e5/jaraco.classes-3.2.3-py3-none-any.whl",
    )
    version(
        "3.2.2",
        sha256="e6ef6fd3fcf4579a7a019d87d1e56a883f4e4c35cfe925f86731abc58804e647",
        url="https://pypi.org/packages/8f/e6/f92d21f915cee7acf1cfe3e0ec60b8e9888dcf40a9814e3838a87ba487d0/jaraco.classes-3.2.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@3.2.2:3.2")
        depends_on("py-more-itertools", when="@3:")
