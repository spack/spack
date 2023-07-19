import os
import re
import shutil
import subprocess

from spack.package import *
from spack.pkg.builtin.singularityce import Singularityce as BuiltinSingularityce


class Singularityce(BuiltinSingularityce):
    __doc__ = BuiltinSingularityce.__doc__

    # BBPP154-53: Depend on HPE-MPI implementation for BB5 to get the expected MPI
    #             performance from the executed images
    depends_on("hpe-mpi", type="run")

    def setup_run_environment(self, env):
        # BBPP154-53: append to SINGULARITY_CONTAINLIBS env variable all the
        #             InfiniBand, NUMA, MLX, and NL libraries
        ldconfig_results = subprocess.run(
            ["ldconfig", "-p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for lib in re.findall(
            r"[\_\-/a-zA-Z0-9]*(?:/libib|/libnuma|/libmlx|/libnl).*\.so[.0-9]*",
            ldconfig_results.stdout.decode("utf-8"),
        ):
            if os.path.isfile(lib):
                env.append_path("SINGULARITY_CONTAINLIBS", lib, separator=",")
        # BBPP154-53: append to SINGULARITY_BINDPATH the path to ldconfing to
        #             avoid segfaulting since we set the `ldconfig path` in the
        #             singularity configuration file in `/etc/singularity/singularity.conf`
        #             This is BB5/RedHat 7 specific
        ldconfig_exe_dir = os.path.dirname(shutil.which("ldconfig"))
        env.append_path(
            "SINGULARITY_BINDPATH", f"{ldconfig_exe_dir}:{ldconfig_exe_dir}:ro", separator=","
        )
