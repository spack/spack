from spack.package import *


class Starship(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://starship.rs"
    url = "https://github.com/starship/starship/releases/download/v1.10.2/starship-x86_64-unknown-linux-gnu.tar.gz"
    maintainers = [
        "andrewda",
        "andytom",
        "ATiltedTree",
        "cappyzawa",
        "davidkna",
        "heyrict",
        "jimleroyer",
        "jletey",
        "kidonng",
        "matchai",
        "Snuggle",
        "tiffafoo",
        "vladimyr",
        "wyze",
    ]

    version("1.10.2", sha256="253a62e48c1b15d5465c876560b71e1d3485697e22ab7adea85e37cbe1a70a54")

    def install(self, spec, prefix):
        make()
        make("install")
