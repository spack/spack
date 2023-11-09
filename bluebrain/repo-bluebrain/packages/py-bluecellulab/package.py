# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluecellulab(PythonPackage):
    """Pythonic Blue Brain simulator access, former BGLibPy"""

    homepage = "https://github.com/BlueBrain/BlueCelluLab"
    pypi = "bluecellulab/bluecellulab-1.5.2.tar.gz"

    version("1.5.2", sha256="22e45b921ad9cd282d53b57ac90fcec69731cb718ed8098c8eb52039bf7a49e5")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("neuron+python@8", type=("build", "run"))
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-matplotlib@3.0.0:", type=("build", "run"))
    depends_on("py-bluepysnap@1.0.7:1", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-pydantic", type=("build", "run"))
    depends_on("py-typing-extensions@4.8.0", type="run")

    # skip import test, because bluecellulab needs HOC_LIBRARY_PATH
    # that could be provided by neurodamus-core
    import_modules = []

    def setup_run_environment(self, env):
        env.set("NEURON_INIT_MPI", "0")
        env.unset("PMI_RANK")
