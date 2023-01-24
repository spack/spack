# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from os.path import dirname as dn


def main(argv=None):
    # Find spack's location and its prefix.
    this_file = os.path.realpath(os.path.expanduser(__file__))
    spack_prefix = dn(dn(dn(dn(this_file))))

    # Allow spack libs to be imported in our scripts
    spack_lib_path = os.path.join(spack_prefix, "lib", "spack")
    sys.path.insert(0, spack_lib_path)

    # Add external libs
    spack_external_libs = os.path.join(spack_lib_path, "external")
    sys.path.insert(0, os.path.join(spack_external_libs, "_vendoring"))
    sys.path.insert(0, spack_external_libs)
    # Here we delete ruamel.yaml in case it has been already imported from site
    # (see #9206 for a broader description of the issue).
    #
    # Briefly: ruamel.yaml produces a .pth file when installed with pip that
    # makes the site installed package the preferred one, even though sys.path
    # is modified to point to another version of ruamel.yaml.
    if "ruamel.yaml" in sys.modules:
        del sys.modules["ruamel.yaml"]

    if "ruamel" in sys.modules:
        del sys.modules["ruamel"]

    import spack.main  # noqa: E402

    sys.exit(spack.main.main(argv))
