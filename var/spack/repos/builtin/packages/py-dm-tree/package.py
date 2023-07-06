# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyDmTree(PythonPackage):
    """tree is a library for working with nested data structures. In a
    way, tree generalizes the builtin map() function which only
    supports flat sequences, and allows to apply a function to each
    leaf preserving the overall structure."""

    homepage = "https://github.com/deepmind/tree"
    pypi = "dm-tree/dm-tree-0.1.5.tar.gz"

    maintainers("aweits")

    version("0.1.8", sha256="0fcaabbb14e7980377439e7140bd05552739ca5e515ecb3119f234acee4b9430")
    version("0.1.7", sha256="30fec8aca5b92823c0e796a2f33b875b4dccd470b57e91e6c542405c5f77fd2a")
    version("0.1.6", sha256="6776404b23b4522c01012ffb314632aba092c9541577004ab153321e87da439a")
    version("0.1.5", sha256="a951d2239111dfcc468071bc8ff792c7b1e3192cab5a3c94d33a8b2bda3127fa")

    depends_on("py-setuptools", type="build")
    depends_on("cmake", when="@0.1.7:", type="build")
    depends_on("bazel@:5", when="@:0.1.6", type="build")
    depends_on("py-six@1.12.0:", when="@:0.1.6", type=("build", "run"))

    # This is set later
    tmp_path = None

    @run_after("install")
    def clean(self):
        remove_linked_tree(PyDmTree.tmp_path)

    def patch(self):
        PyDmTree.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["TEST_TMPDIR"] = PyDmTree.tmp_path
        env["HOME"] = PyDmTree.tmp_path
        args = [
            # Don't allow user or system .bazelrc to override build settings
            "'--nohome_rc',\n",
            "'--nosystem_rc',\n",
            # Bazel does not work properly on NFS, switch to /tmp
            "'--output_user_root={0}',\n".format(PyDmTree.tmp_path),
            "'build',\n",
            # Spack logs don't handle colored output well
            "'--color=no',\n",
            "'--jobs={0}',\n".format(make_jobs),
            # Enable verbose output for failures
            "'--verbose_failures',\n",
            # Show (formatted) subcommands being executed
            "'--subcommands=pretty_print',\n",
            "'--spawn_strategy=local',\n",
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            "'--explain=explainlogfile.txt',\n",
            # Increase verbosity of explanation,
            "'--verbose_explanations',\n",
            # bazel uses system PYTHONPATH instead of spack paths
            "'--action_env', 'PYTHONPATH={0}',\n".format(env["PYTHONPATH"]),
        ]
        filter_file("'build',", " ".join(args), "setup.py")
