# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOmpcbMerge(PythonPackage):
    """Command-line tool to merge trace timelines from OMPC runtime."""

    homepage = "https://gitlab.com/ompcluster/ompcbench"

    url = "https://github.com/VitoriaDMP/ompcb-merge/raw/master/ompcb-merge-1.0.tar.gz"

    maintainers("VitoriaDMP")

    version("1.0", sha256="807a311e93fe5063058194a75612dbabc26dfcde19adef33ba71fa72191c8d39")

    depends_on("py-orjson@3.6:", type=("build"))
    depends_on("py-click@8.0:", type=("build"))

    depends_on("py-setuptools", type="build")
