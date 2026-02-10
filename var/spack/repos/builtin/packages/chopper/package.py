#     spack install chopper
#
# You can edit this file again by typing:
#
#     spack edit chopper
#
# See the Spack documentation for more information on packaging.
# ---------------------------------------------------------------------------
from spack.package import *


class Chopper(Package):
    """Rust implementation of long read trimming and filtering."""

    homepage = "https://github.com/wdecoster/chopper/"
    url = "https://github.com/wdecoster/chopper/releases/download/v0.12.0b/chopper-linux"

    maintainers = ["josue-iac"]

    version("0.12.0b", sha256="183c1a344227b0f07e62a697d4c16c43548d68262d03bf5b2fda68e13ea47eb2", expand=False)
    version("0.12.0", sha256="892f57a4a9d085eb983e1f1a9755b275220f200be13a8cc314ddff361a69eb71", expand=False)
    version("0.11.0", sha256="d9d7e4c62e5568e0499201efda441ca23b52f92c024b09fb58c0657270d51446", expand=False)
    version("0.10.0b", sha256="9c7c707f8de594f5d7afcdb1001ff84b62ac5c86d318c6c9b6d0260257f52382", expand=False)

    # O Spack baixa o ficheiro como 'chopper-linux'
    # Nós instalamos na pasta final como 'chopper'

    def install(self, spec, prefix):
        # Cria a pasta bin
        mkdirp(prefix.bin)
        
        # Define o caminho de destino de forma simples
        dest = join_path(prefix.bin, "chopper")
        
        # Instala o binário literal baixado
        install("chopper-linux", dest)
        
        # Torna o binário executável
        set_executable(dest)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
