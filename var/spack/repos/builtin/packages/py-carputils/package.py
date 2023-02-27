# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCarputils(PythonPackage):
    """The carputils framework for running simulations with the openCARP software."""

    homepage = "https://www.opencarp.org"
    git = "https://git.opencarp.org/openCARP/carputils.git"

    maintainers("MarieHouillon")

    version("master", branch="master")
    # Version to use with openCARP releases
    version("oc12.0", commit="4d7a1f0c604a2ad232e70cf9aa3a8daff5ffb195")
    version("oc11.0", commit="a02f9b846c6e852b7315b20e925d55c355f239b8")
    version("oc10.0", commit="a02f9b846c6e852b7315b20e925d55c355f239b8")
    version("oc9.0", commit="e79e66b25c7bfaf405fad595019594ab9aa83392")
    version("oc8.2", commit="e60f639c0f39ad71c8ae11814de1f3aa726e8352")
    version("oc8.1", commit="a4210fcb0fe17226a1744ee9629f85b629decba3")
    version("oc7.0", commit="4c04db61744f2fb7665594d7c810699c5c55c77c")

    depends_on("git")

    depends_on("python", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type="run")
    depends_on("py-scipy@1.5.0:", type="run")
    depends_on("py-matplotlib@3.0.0:", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-tables@3.6.1:", type="run")
    depends_on("py-six@1.12.0:", type="run")
    depends_on("py-ruamel-yaml", type="run")
