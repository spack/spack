# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyFitter(PythonPackage):
    """fitter package provides a simple class to identify the distribution
    from which a data samples is generated from. It uses 80 distributions
    from Scipy and allows you to plot the results to check what is the
    most probable distribution and the best parameters."""

    homepage = "https://github.com/cokelaer/fitter"
    pypi = "fitter/fitter-1.5.1.tar.gz"

    maintainers("carsonwoods")

    version("1.6.0", sha256="908223d75b35d3846984bfb2fed1d2a926da5a30b95b704aa95b2a894227c0af")
    version("1.5.2", sha256="afb33a8b1e24cdbc9318f55be72534e07028f25240ab76a4b081d27d1ed677d9")
    version("1.5.1", sha256="893b35ad0a84c3b96b63ec203a6a79effdba98777aed966ae61709f5e1e8cf99")

    depends_on("py-setuptools", type="build")

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy@0.18:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
