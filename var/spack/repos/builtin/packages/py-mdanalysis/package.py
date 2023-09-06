# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdanalysis(PythonPackage):
    """MDAnalysis is a Python toolkit to analyze molecular dynamics
    trajectories generated by a wide range of popular simulation
    packages including DL_Poly, CHARMM, Amber, NAMD, LAMMPS, and
    Gromacs. (See the lists of supported trajectory formats and
    topology formats.)"""

    homepage = "https://www.mdanalysis.org"
    pypi = "MDAnalysis/MDAnalysis-2.4.2.tar.gz"

    maintainers("RMeli")

    version("2.6.1", sha256="9cc69b94bddd026f26ffcaf5bdbed6d568c1c10e19a341d84f8d37a2a70222f2")
    version("2.6.0", sha256="210b198a115165004c36fbbbe5eb83a13323f52b10ccaef30dd40bfe25ba3e61")
    version("2.5.0", sha256="06ce4efab6ca1dbd2ee2959fc668049e1d574a8fe94ab948a4608244da1d016b")
    version("2.4.3", sha256="c4fbdc414e4fdda69052fff2a6e412180fe6fa90a42c24793beee04123648c92")
    version("2.4.2", sha256="ae2ee5627391e73f74eaa3c547af3ec6ab8b040d27dedffe3a7ece8e0cd27636")

    variant(
        "analysis",
        default=True,
        description="Enable analysis packages: matplotlib, scipy, seaborn",
    )
    variant("extra_formats", default=False, description="Support extra formats")

    depends_on("python@3.9:", type=("build", "run"), when="@2.5.0:")
    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-cython@0.28:", type="build")

    # MDAnalysis required dependencies (install_requires)
    depends_on("py-numpy@1.22.3:1", when="@2.6.0:", type=("build", "run"))
    depends_on("py-numpy@1.21.0:", when="@2.5.0:", type=("build", "run"))
    depends_on("py-numpy@1.20.0:", type=("build", "run"))

    depends_on("py-biopython@1.80:", type=("build", "run"))
    depends_on("py-networkx@2.0:", type=("build", "run"))
    depends_on("py-griddataformats@0.4.0:", type=("build", "run"))
    depends_on("py-mmtf-python@1.0.0:", type=("build", "run"))
    depends_on("py-joblib@0.12:", type=("build", "run"))

    depends_on("py-scipy@1.5.0:", type=("build", "run"))

    depends_on("py-matplotlib@1.5.1:", type=("build", "run"))
    depends_on("py-tqdm@4.43.0:", type=("build", "run"))
    depends_on("py-threadpoolctl", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-fasteners", type=("build", "run"))
    depends_on("py-gsd@1.9.3:", when="@:2.5.0", type=("build", "run"))

    # extra_format (extras_require)
    depends_on("py-netcdf4@1.0:", when="+extra_formats", type=("build", "run"))
    depends_on("py-h5py@2.10:", when="+extra_formats", type=("build", "run"))
    depends_on("py-pytng@0.2.3:", when="+extra_formats", type=("build", "run"))
    depends_on("py-chemfiles@0.10:", when="+extra_formats", type=("build", "run"))
    depends_on("py-pyedr@0.7.0:", when="+extra_formats", type=("build", "run"))
    #    depends_on("py-gsd@3.0.1:", when="+extra_formats @2.6.0:", type=("build", "run"))
    depends_on(
        "rdkit@2020.03.1: +python ~coordgen ~maeparser ~yaehmop ~descriptors3d",
        when="+extra_formats @2.6.0:",
        type=("build", "run"),
    )
    depends_on("py-parmed", when="+extra_formats @2.6.0:", type=("build", "run"))

    # analysis (extras_require)
    depends_on("py-seaborn", when="+analysis", type=("build", "run"))
    depends_on("py-scikit-learn", when="+analysis", type=("build", "run"))
    depends_on("py-tidynamics@1:", when="+analysis", type=("build", "run"))
