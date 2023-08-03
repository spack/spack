# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Drishti(PythonPackage):
    """
    Drishti is a command-line tool to guide end-users in optimizing I/O in their applications
    by detecting typical I/O performance pitfalls and providing a set of recommendations.
    """

    homepage = "https://github.com/hpc-io/drishti-io"
    git = "https://github.com/hpc-io/drishti-io"
    pypi = "drishti-io/drishti-io-0.6.tar.gz"

    maintainers("jeanbez", "sbyna")

    version("master", branch="master")

    version("0.6", sha256="f1883e48de4a863f284f9c54febd2b04d04456848aea3e34c355310a3336e3b8")
    version("0.5", sha256="08ae82dfa82872cde1f0a219e979b9c10d6c4a01f762066ea864a400cc144d78")
    version("0.4", sha256="bbbb272b4f6f44ae762f6cba28a2c589e15608691c559af0cc2f552590335d7b")

    depends_on("darshan-util@3.4:", type=("run", "test"))

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-rich@12.5.1", type=("build", "run"))
    depends_on("py-darshan@3.4:", type=("build", "run"))

    def test_help(self):
        """Run drishti help."""
        drishti = which(self.prefix.bin.drishti)
        drishti("-h")