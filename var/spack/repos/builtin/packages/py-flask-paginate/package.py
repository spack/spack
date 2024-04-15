# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskPaginate(PythonPackage):
    """Simple paginate for flask (study from will_paginate). Use bootstrap css
    framework, supports bootstrap2&3 and foundation."""

    homepage = "https://github.com/lixxu/flask-paginate"
    pypi = "flask-paginate/flask-paginate-2022.1.8.tar.gz"

    maintainers("meyersbs")

    license("BSD-3-Clause")

    version(
        "2022.1.8",
        sha256="b3fc28752b8e0546999f3d4b0678351ae3230ea4424353c59db9f0d479fd9049",
        url="https://pypi.org/packages/94/d5/5610ce12fcd5985d4ad8e868c6a1de9862f3a6fdf3a5dd15925b7d968a22/flask_paginate-2022.1.8-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-flask")
