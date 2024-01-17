# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from llnl.util.filesystem import copy_tree, mkdirp, remove_linked_tree, touchp, working_dir

import spack.config
import spack.main
from spack.package import *


class SpackManager(Package):
    """Spack extension for managing application configurations and environment curation across multiple software applications"""

    homepage = "https://sandialabs.github.io/spack-manager"
    git = "https://github.com/sandialabs/spack-manager"

    maintainers("psakievich")

    version("develop", branch="develop")

    # everything below here is generic
    scopes = list(spack.config.scopes().keys())
    scopes.remove("_builtin")
    scopes.remove("command_line")
    scopes.insert(0, "none")
    variant(
        "scopes",
        default="none",
        description="scopes to register the spack-manager extension",
        values=scopes,
        multi=True,
    )

    def install(self, spec, prefix):
        # copy all files from stage to $prefix/spack-manager
        extension_path = os.path.join(prefix, spec.name)
        mkdirp(extension_path)
        copy_tree(self.stage.source_path, extension_path)
        config = spack.main.SpackCommand("config")
        for scope in self.spec.variants["scopes"].value:
            if scope != "none":
                register_args = ["--scope", scope]
                register_args.extend(["add", "config:extensions:[{0}]".format(extension_path)])
                config(*register_args)

    @run_before("uninstall")
    def pre_uninstall(spec):
        breakpoint()
        print("CLEANUP HAPPENING")
        config = spack.main.SpackCommand("config")
        extension_path = os.path.join(spec.prefix, spec.name)
        for scope in spec.variants["scopes"].value:
            if scope != "none":
                rm_args = ["--scope", scope]
                rm_args.extend(["rm", "config:extensions:[{0}]".format(extension_path)])
                config(*rm_args)

    @run_after("uninstall")
    def cleanup(self):
        breakpoint()
        print("CLEANUP HAPPENING")
        config = spack.main.SpackCommand("config")
        extension_path = os.path.join(self.spec.prefix, self.spec.name)
        for scope in self.spec.variants["scopes"].value:
            if scope != "none":
                rm_args = ["--scope", scope]
                rm_args.extend(["rm", "config:extensions:[{0}]".format(extension_path)])
                config(*rm_args)
        # super().do_uninstall(force=force)
