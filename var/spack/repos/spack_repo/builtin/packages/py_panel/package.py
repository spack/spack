# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPanel(PythonPackage):
    """A high level app and dashboarding solution for Python."""

    homepage = "https://panel.holoviz.org/"
    pypi = "panel/panel-0.14.4.tar.gz"

    license("BSD-3-Clause")

    version("1.6.3a2", sha256="c4413f8f604c7457b4f0fe7b3d375cc8cdeeacdbf01480b89cd00a49453a734a")
    version("1.5.2", sha256="30a45f314716bdde2de5c002fbd3a0b4d6ff85459e2179284df559455ff1534b")
    version("0.14.4", sha256="b853d2f53d7738ec6372525360c5bf9427a71ed990685ccac703bc9b442e9951")

    depends_on("python@3.7:", type=("build", "run"), when="@0.14.4")
    depends_on("python@3.10:", type=("build", "run"), when="@1.5.2:")

    depends_on("py-pyct@0.4.4:", type=("build", "run"), when="@0.14.4")
    depends_on("py-setuptools@42:", type=("build", "run"), when="@0.14.4")

    depends_on("py-hatchling", type="build", when="@1.5.2:")
    depends_on("py-hatch-vcs", type="build", when="@1.5.2:")

    depends_on("py-bokeh@2.4.3:2.4", type=("build", "run"), when="@0.14.4")
    depends_on("py-bokeh@3.5:3.6", type=("build", "run"), when="@1.5.2:")
    depends_on("py-bokeh@3.5:3.7", type=("build", "run"), when="@1.6.3:")

    depends_on("py-param@1.12:", type=("build", "run"), when="@0.14.4")
    depends_on("py-param@2.1:2", type=("build", "run"), when="@1.5.2:")

    depends_on("py-pyviz-comms@0.7.4:", type=("build", "run"), when="@0.14.4")
    depends_on("py-pyviz-comms@2:", type=("build", "run"), when="@1.5.2:")

    depends_on("py-markdown")
    depends_on("py-markdown-it-py", type=("build", "run"), when="@1.5.2:")
    depends_on("py-linkify-it-py", type=("build", "run"), when="@1.5.2:")
    depends_on("py-mdit-py-plugins", type=("build", "run"), when="@1.5.2:")
    depends_on("py-requests")

    depends_on("py-bleach", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    depends_on("py-packaging")
    depends_on("py-pandas@1.2:", type=("build", "run"), when="@1.5.2:")
    depends_on("py-tqdm@4.48:", type=("build", "run"))

    # Version 18 or later are requested by py-panel
    depends_on("node-js@18:", type=("build", "run"))
    # Version 9 is not requested explicitly, it's
    # a guess that the more recent version of node-js
    # should go with a more recent version of npm
    depends_on("npm@9:", type=("build", "run"))
