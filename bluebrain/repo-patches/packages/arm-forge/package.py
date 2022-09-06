from spack.package import *
from spack.pkg.builtin.arm_forge import ArmForge as BuiltinArmForge


class ArmForge(BuiltinArmForge):
    __doc__ = BuiltinArmForge.__doc__

    version(
        "22.0.3-Linux-x86_64",
        sha256="4dc8d0bb3923810cf78279dd446d5a529af523271111249b795cef01f86bd0fd",
        url="https://content.allinea.com/downloads/arm-forge-22.0.3-linux-x86_64.tar",
    )

    def setup_run_environment(self, env):
        # ENV variables required to avoid licensing and SLURM issues on BB5
        env.unset('HTTP_PROXY')
        env.unset('HTTPS_PROXY')
        env.unset('http_proxy')
        env.unset('https_proxy')
        env.set('ALLINEA_USE_SSH_STARTUP', "1")
