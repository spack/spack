# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Refs for building from source and recipes
# https://alps.comp-phys.org/mediawiki/index.php/Building_ALPS_from_source
# https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs/a/ALPS
# https://github.com/conda-forge/alps-feedstock/tree/master/recipe


class Alps(CMakePackage):
    """Algorithms for Physics Simulations

    Tags: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://alps.comp-phys.org"
    url = "https://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"

    version(
        "20220304_r7871", sha256="74bcb9156701f81439af3c60ecf26afeb6458c48012729aea2e9f7aa34e87426"
    )
    # version 2.3.0 is removed since it requires python@:3.6 that's not supported by Spack

    # build fails as of boost@1.83
    depends_on(
        "boost@:1.82.0"
        "+chrono +date_time +filesystem +iostreams +mpi +numpy +program_options"
        "+python +regex +serialization +system +test +thread +timer"
    )
    depends_on("fftw")
    depends_on("hdf5 ~mpi+hl")
    depends_on("lapack")
    depends_on("python", type=("build", "link", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))

    extends("python")

    def url_for_version(self, version):
        if str(version) == "2.3.0":
            url = "https://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"
        elif str(version) == "20220304_r7871":
            url = "http://exa.phys.s.u-tokyo.ac.jp/archive/MateriApps/src/alps_20220304~r7871.orig.tar.gz"
        return url

    def cmake_args(self):
        args = []
        args.append("Boost_ROOT_DIR=" + self.spec["boost"].prefix)
        args.append("-DCMAKE_CXX_FLAGS={0}".format(self.compiler.cxx98_flag))
        return args

    def _single_test(self, target, exename, dataname, opts=[]):
        troot = self.prefix.tutorials
        copy_tree(join_path(troot, target), target)

        if target == "dmrg-01-dmrg":
            test_dir = self.test_suite.current_test_data_dir
            copy(join_path(test_dir, dataname), target)

        self.run_test("parameter2xml", options=[dataname, "SEED=123456"], work_dir=target)
        options = []
        options.extend(opts)
        options.extend(["--write-xml", "{0}.in.xml".format(dataname)])
        self.run_test(
            exename, options=options, expected=["Finished with everything."], work_dir=target
        )

    def test(self):
        self._single_test("mc-02-susceptibilities", "spinmc", "parm2a", ["--Tmin", "10"])
        self._single_test("ed-01-sparsediag", "sparsediag", "parm1a")
        self._single_test("dmrg-01-dmrg", "dmrg", "spin_one_half")
