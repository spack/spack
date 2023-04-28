# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib
import shutil

from spack.package import *


class Roentdek(Package):
    """Software for Roentdek detector."""

    homepage = "https://www.roentdek.com"
    url = "https://pswww.slac.stanford.edu/swdoc/tutorials/hexanode-proxy-0.0.3.tar.gz"

    maintainers = ["valmar"]

    version("0.0.3", sha256="8d88cf4edaddd6ff8befabd916a49e0ac884b2dccd318f6c36953647c30b0506")

    def install(self, spec, prefix):
        base_path = pathlib.Path(prefix)

        pathlib.Path(base_path / "lib").mkdir(parents=True)
        pathlib.Path(base_path / "include" / "roentdek").mkdir(parents=True)

        shutil.copyfile(
            "x86_64-centos7-gcc731/resort64c.h", base_path / "include" / "roentdek" / "resort64c.h"
        )
        shutil.copyfile(
            "x86_64-centos7-gcc731/libResort64c_x64.a", base_path / "lib" / "libResort64c_x64.a"
        )
