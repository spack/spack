# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeedir(PythonPackage):
    """Seedir is a Python package for creating, editing, and reading folder tree diagrams."""

    homepage = "https://earnestt1234.github.io/seedir/seedir/index.html"
    pypi = "seedir/seedir-0.4.2.tar.gz"
    git = "https://github.com/earnestt1234/seedir.git" 

    version("0.4.2", sha256="a549896f37fb31243cf9c8f44405821d9176b2b0c91804f87b7018ea0a738d2b")
    version("0.3.1", sha256="bbf6aef0fa51cd7e6ba8bdaff67a0913bc7199cd6302a92676fbae409112db54")
    version("0.2.0", sha256="49d89cb6074267dc76e7048cc5f2904c5eef8657c206d2086ecdd96ba89fc6d6")

    depends_on("python@3.8:", type=("build", "run")) 
    depends_on("py-natsort", type=("build", "run")) 
    depends_on("py-emoji", type=("build", "run")) 
