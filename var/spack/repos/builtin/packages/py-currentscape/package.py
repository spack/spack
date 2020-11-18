# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCurrentscape(PythonPackage):
    """Module to easily plot currentscape."""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/cells/currentscape"
    url = "ssh://bbpcode.epfl.ch/cells/currentscape"
    git = "ssh://bbpcode.epfl.ch/cells/currentscape"

    version("develop", branch="master")
    version("0.0.2", tag="0.0.2")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-scipy", type="run")
