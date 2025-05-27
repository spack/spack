# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyWarcio(PythonPackage):
    """Streaming WARC/ARC library for fast web archive IO."""

    homepage = "https://github.com/webrecorder/warcio"
    pypi = "warcio/warcio-1.7.5.tar.gz"

    version("1.7.5", sha256="7247b57e68074cfd9433cb6dc226f8567d6777052abec2d3c78346cffa4d19b9")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
