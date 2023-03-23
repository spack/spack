# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrsistent(PythonPackage):
    """Pyrsistent is a number of persistent collections
    (by some referred to as functional data structures).
    Persistent in the sense that they are immutable."""

    homepage = "https://github.com/tobgu/pyrsistent/"
    pypi = "pyrsistent/pyrsistent-0.15.7.tar.gz"

    version("0.18.1", sha256="d4d61f8b993a7255ba714df3aca52700f8125289f84f704cf80916517c46eb96")
    version("0.18.0", sha256="773c781216f8c2900b42a7b638d5b517bb134ae1acbebe4d1e8f1f41ea60eb4b")
    version("0.16.0", sha256="28669905fe725965daa16184933676547c5bb40a5153055a8dee2a4bd7933ad3")
    version("0.15.7", sha256="cdc7b5e3ed77bed61270a47d35434a30617b9becdf2478af76ad2c6ade307280")

    depends_on("python@2.7:2.8,3.5:", type=("build", "link", "run"))
    depends_on("python@3.6:", when="@0.18.0:", type=("build", "link", "run"))
    depends_on("python@3.7:", when="@0.18.1:", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@42:", when="@0.18.0:", type="build")
    depends_on("py-six", when="@:0.17", type=("build", "run"))
