# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import archspec

from spack.package import *


class Blast2go(Package):
    """Blast2GO is a bioinformatics platform for high-quality functional
    annotation and analysis of genomic datasets."""

    homepage = "https://www.blast2go.com/"

    version("5.2.5", sha256="c37aeda25f96ac0553b52da6b5af3167d50671ddbfb3b39bcb11afe5d0643891")

    for t in {str(x.family) for x in archspec.cpu.TARGETS.values() if str(x.family) != "x86_64"}:
        conflicts(f"target={t}:", msg="blast2go is available x86_64 only")

    depends_on("bash", type="build")
    depends_on("blast-plus", type="run")
    depends_on("java", type="build")

    def url_for_version(self, version):
        return f"http://resources.biobam.com/software/blast2go/nico/Blast2GO_unix_{version.underscored}.zip"

    def install(self, spec, prefix):
        # blast2go install script prompts for the following:
        #
        # continue? [o/c] => o
        # installation prefix => prefix
        # desktop icon [y/n] => n
        # run blast2go? [y/n] => n

        config_input_file = "spack-config.in"

        config_input_data = ["o\n", prefix.bin + "\n", "n\n", "n\n"]

        with open(config_input_file, "w") as f:
            f.writelines(config_input_data)

        with open(config_input_file) as f:
            bash = which("bash")
            bash(f"Blast2GO_unix_{self.version.underscored}.sh", input=f)
