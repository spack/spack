# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchVcs(PythonPackage):
    """Hatch plugin for versioning with your preferred VCS"""

    homepage = "https://github.com/ofek/hatch-vcs"
    pypi = "hatch_vcs/hatch_vcs-0.2.0.tar.gz"

    version("0.2.0", sha256="9913d733b34eec9bb0345d0626ca32165a4ad2de15d1ce643c36d09ca908abff")

    depends_on("py-hatchling@0.21.0:", type=("build", "run"))
    depends_on("py-setuptools-scm@6.4.0:", type=("build", "run"))
