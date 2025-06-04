# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPygraphviz(PythonPackage):
    """Python interface to Graphviz"""

    homepage = "https://pygraphviz.github.io/"
    pypi = "pygraphviz/pygraphviz-1.7.zip"

    maintainers("haralmha")

    license("BSD-3-Clause")

    version("1.14", sha256="c10df02377f4e39b00ae17c862f4ee7e5767317f1c6b2dfd04cea6acc7fc2bea")
    version("1.13", sha256="6ad8aa2f26768830a5a1cfc8a14f022d13df170a8f6fdfd68fd1aa1267000964")
    version("1.12", sha256="8b0b9207954012f3b670e53b8f8f448a28d12bdbbcf69249313bd8dbe680152f")
    version("1.11", sha256="a97eb5ced266f45053ebb1f2c6c6d29091690503e3a5c14be7f908b37b06f2d4")
    version("1.10", sha256="457e093a888128903251a266a8cc16b4ba93f3f6334b3ebfed92c7471a74d867")
    version("1.7", sha256="a7bec6609f37cf1e64898c59f075afd659106cf9356c5f387cecaa2e0cdb2304")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:", when="@1.10:", type=("build", "run"))
    depends_on("python@3.10:", when="@1.12:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("graphviz")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/p/pygraphviz/pygraphviz-{}.{}"
        if version >= Version("1.12"):
            fext = "tar.gz"
        else:
            fext = "zip"
        return url.format(version, fext)

    # graphviz isn't detected during install.
    def patch(self):
        inc_dir = self["graphviz"].prefix.include
        lib_dir = self.spec["graphviz"].libs.directories[0]
        filter_file("include_dirs=[],", f'include_dirs = ["{inc_dir}"],', "setup.py", string=True)
        filter_file("library_dirs=[],", f'library_dirs = ["{lib_dir}"],', "setup.py", string=True)
