# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTrafilatura(PythonPackage):
    """Python & Command-line tool to gather text and metadata on the Web:
    Crawling, scraping, extraction, output as CSV, JSON, HTML, MD, TXT, XML."""

    homepage = "https://trafilatura.readthedocs.io"
    pypi = "trafilatura/trafilatura-1.11.0.tar.gz"

    license("Apache-2.0")

    version("1.11.0", sha256="9334ca101c40b2904af5afcee790f0374fabca3ac388811720be65cc768787a2")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@61.0:", type="build")

    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-charset-normalizer@3.2.0:", type=("build", "run"))
    depends_on("py-courlan@1.1.0:", type=("build", "run"))
    depends_on("py-htmldate@1.8.1:", type=("build", "run"))
    depends_on("py-justext@3.0.1:", type=("build", "run"))
    depends_on("py-urllib3@1.26:2", type=("build", "run"))
    depends_on("py-lxml@4.9.2", when="platform=darwin ^python@3.8", type=("build", "run"))
    depends_on("py-lxml@5.3.0:", when="platform=linux", type=("build", "run"))
    depends_on("py-lxml@5.3.0:", when="^python@3.9:", type=("build", "run"))
