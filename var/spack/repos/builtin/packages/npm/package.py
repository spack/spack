# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack.package import *


class Npm(Package):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/cli"
    # base https://www.npmjs.com/

    git = "https://github.com/npm/cli.git"
    url = "https://registry.npmjs.org/npm/-/npm-9.3.1.tgz"

    version("9.3.1", sha256="41caa26a340b0562bc5429d28792049c980fe3e872b42b82cad94e8f70e37f40")
    version("8.19.3", sha256="634bf4e0dc87be771ebf48a058629960e979a209c20a51ebdbc4897ca6a25260")
    version("7.24.2", sha256="5b9eeea011f8bc3b76e55cc33339e87213800677f37e0756ad13ef0e9eaccd64")
    version("6.14.18", sha256="c9b15f277e2a0b1b57e05bad04504296a27024555d56c2aa967f862e957ad2ed")

    version(
        "6.14.9",
        sha256="1e0e880ce0d5adf0120fb3f92fc8e5ea5bac73681d37282615d074ff670f7703",
        deprecated=True,
    )
    version(
        "6.14.8",
        sha256="fe8e873cb606c06f67f666b4725eb9122c8927f677c8c0baf1477f0ff81f5a2c",
        deprecated=True,
    )
    version(
        "6.13.7",
        sha256="6adf71c198d61a5790cf0e057f4ab72c6ef6c345d72bed8bb7212cb9db969494",
        deprecated=True,
    )
    version(
        "6.13.4",
        sha256="a063290bd5fa06a8753de14169b7b243750432f42d01213fbd699e6b85916de7",
        deprecated=True,
    )
    version(
        "3.10.9",
        sha256="fb0871b1aebf4b74717a72289fade356aedca83ee54e7386e38cb51874501dd6",
        deprecated=True,
    )
    version(
        "3.10.5",
        sha256="ff019769e186152098841c1fa6325e5a79f7903a45f13bd0046a4dc8e63f845f",
        deprecated=True,
    )

    depends_on("node-js", type=("build", "run"))
    depends_on("libvips")

    # npm 6.13.4 ships with node-gyp 5.0.5, which contains several Python 3
    # compatibility issues on macOS. Manually update to node-gyp 6.0.1 for
    # full Python 3 support.
    resource(
        name="node-gyp",
        destination="node-gyp",
        url="https://registry.npmjs.org/node-gyp/-/node-gyp-6.0.1.tgz",
        sha256="bbc0e137e17a63676efc97a0e3b1fcf101498a1c2c01c3341cd9491f248711b8",
        when="@6",
    )
    resource(
        name="env-paths",
        destination="env-paths",
        url="https://registry.npmjs.org/env-paths/-/env-paths-2.2.0.tgz",
        sha256="168b394fbca60ea81dc84b1824466df96246b9eb4d671c2541f55f408a264b4c",
        when="@6",
    )

    @when("@6")
    def patch(self):
        shutil.rmtree("node_modules/node-gyp")
        install_tree("node-gyp/package", "node_modules/node-gyp")
        filter_file(r'"node-gyp": "\^5\..*"', '"node-gyp": "^6.0.1"', "package.json")
        install_tree("env-paths/package", "node_modules/env-paths")

    @when("@:8")
    def install(self, spec, prefix):
        # `npm install .` doesn't work properly out of the box on npm up to 8, so we do
        # what it would do manually. The only thing we seem to miss is docs. In
        # particular, it will end up symlinking into the stage, which spack then
        # deletes. You can avoid that with `npm install $(npm pack .)`, but `npm pack`
        # also seems to fail when run from the tarball on macos. So we just copy manually.
        to_install = [
            "LICENSE",
            "README.md",
            "bin",
            "docs",
            "index.js",
            "lib",
            "node_modules",
            "package.json",
        ]

        mkdirp(prefix.bin)
        mkdirp(prefix.lib.node_modules.npm)

        # manually install all the files above (if they exist for a particular node version)
        for filename in to_install:
            if os.path.exists(filename):
                install_fn = install if os.path.isfile(filename) else install_tree
                install_fn(filename, os.path.join(prefix.lib.node_modules.npm, filename))

        # set up symlinks in bin
        node_modules_bin = os.path.relpath(prefix.lib.node_modules.npm.bin, prefix.bin)
        symlink(os.path.join(node_modules_bin, "npm-cli.js"), prefix.bin.npm)
        symlink(os.path.join(node_modules_bin, "npx-cli.js"), prefix.bin.npx)

    @when("@9:")
    def install(self, spec, prefix):
        # in npm 9, `npm install .` finally works within the repo, so we can just call it.
        node = which("node", required=True)
        node("bin/npm-cli.js", "install", "-ddd", "--global", f"--prefix={prefix}", ".")

    def setup_dependent_build_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdirp(npm_config_cache_dir)
        env.set("npm_config_cache", npm_config_cache_dir)

    def setup_dependent_run_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        env.set("npm_config_cache", npm_config_cache_dir)
