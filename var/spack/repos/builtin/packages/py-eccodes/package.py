# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEccodes(PythonPackage):
    """Python interface to the ecCodes GRIB and BUFR decoder/encoder."""

    homepage = "https://github.com/ecmwf/eccodes-python"
    pypi = "eccodes/eccodes-1.3.2.tar.gz"

    version("1.5.0", sha256="e70c8f159140c343c215fd608ddf533be652ff05ad2ff17243c7b66cf92127fa")
    version("1.3.2", sha256="f282adfdc1bc658356163c9cef1857d4b2bae99399660d3d4fcb145a52d3b2a6")

    variant("hardcode-path", default=False, description="Hardcore path to the ecCodes library")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-attrs", type=("build", "run"))
    depends_on("py-cffi", type=("build", "run"))
    depends_on("py-findlibs", type=("build", "run"), when="~hardcode-path")
    depends_on("eccodes@2.21.0:+shared", type="run")

    # Hardcode path to libeccodes with value @ECCODES_PATH@ to be replaced with the real path to
    # the library in the following patch method:
    patch("hardcode-path.patch", when="+hardcode-path")

    @when("+hardcode-path")
    def patch(self):
        filter_file(
            "@ECCODES_PATH@",
            self.spec["eccodes:c,shared"].libs.files[0],
            "gribapi/bindings.py",
            string=True,
            backup=False,
            ignore_absent=False,
        )

    def setup_build_environment(self, env):
        if "~hardcode-path" in self.spec:
            eccodes_libs = self.spec["eccodes:c,shared"].libs
            # ECCODES_HOME has the highest precedence when searching for the library with
            # py-findlibs:
            env.set("ECCODES_HOME", eccodes_libs.directories[0])
            # but not if ecmwflibs (https://pypi.org/project/ecmwflibs/) is in the PYTHONPATH for
            # whatever reason:
            env.set("ECMWFLIBS_ECCODES", eccodes_libs.files[0])

    def setup_run_environment(self, env):
        self.setup_build_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_build_environment(env)

    def test(self):
        super(PyEccodes, self).test()

        self.run_test(
            self.spec["python"].command.path,
            ["-m", "eccodes", "selfcheck"],
            purpose="checking system setup",
            work_dir="spack-test",
        )
