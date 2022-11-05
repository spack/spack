# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsijPython(PythonPackage):
    """ PSI/J is an abstraction layer over cluster schedulers to write scheduler
    agnostic HPC applications."""

    homepage = "https://exaworks.org/"
    git = "https://github.com/exaworks/psij-python.git"
    pypi = "https://files.pythonhosted.org/packages/8d/5b/5e7a36d1d8860c43d6cab7f9eaba6febe9b0328d554da200fa5c7d4a0c98/psij-python-0.1.0.post1.tar.gz"

    maintainers = ["andre-merzky"]

    version("0.1.0", sha256="b59a864ddbaacd06d5e226001bcc0530fea8c161")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-filelock", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
  # depends_on("py-pystache", type=("build", "run"))
