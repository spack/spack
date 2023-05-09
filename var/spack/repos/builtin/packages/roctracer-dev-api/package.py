# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RoctracerDevApi(Package):
    """ROC-tracer API. Installs the API header files of the roctracer-dev
    package, mainly to avoid circular dependencies in the ROCm ecosystem.
    For the ROC-tracer library, please check out roctracer-dev."""

    homepage = "https://github.com/ROCm-Developer-Tools/roctracer"
    git = "https://github.com/ROCm-Developer-Tools/roctracer.git"
    url = "https://github.com/ROCm-Developer-Tools/roctracer/archive/refs/tags/rocm-5.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")

    version("5.4.3", sha256="6b5111be5efd4d7fd6935ca99b06fab19b43d97a58d26fc1fe6e783c4de9a926")
    version("5.4.0", sha256="04c1e955267a3e8440833a177bb976f57697aba0b90c325d07fc0c6bd4065aea")
    version("5.3.3", sha256="f2cb1e6bb69ea1a628c04f984741f781ae1d8498dc58e15795bb03015f924d13")
    version("5.3.0", sha256="36f1da60863a113bb9fe2957949c661f00a702e249bb0523cda1fb755c053808")
    version("5.2.3", sha256="93f4bb7529db732060bc12055aa10dc346a459a1086cddd5d86c7b509301be4f")
    version("5.2.1", sha256="e200b5342bdf840960ced6919d4bf42c8f30f8013513f25a2190ee8767667e59")
    version("5.2.0", sha256="9747356ce61c57d22c2e0a6c90b66a055e435d235ba3459dc3e3f62aabae6a03")
    version("5.1.3", sha256="45f19875c15eb609b993788b47fd9c773b4216074749d7744f3a671be17ef33c")
    version("5.1.0", sha256="58b535f5d6772258190e4adcc23f37c916f775057a91b960e1f2ee1f40ed5aac")
    version(
        "5.0.2",
        sha256="5ee46f079e57dfe491678ffa4cdaf5f3b3d179cb3137948e4bcafca99ded47cc",
        deprecated=True,
    )
    version(
        "5.0.0",
        sha256="a21f4fb093cee4a806d53cbc0645d615d89db12fbde305e9eceee7e4150acdf2",
        deprecated=True,
    )
    version(
        "4.5.2",
        sha256="7012d18b79736dbe119161aab86f4976b78553ce0b2f4753a9386752d75d5074",
        deprecated=True,
    )
    version(
        "4.5.0",
        sha256="83dcd8987e129b14da0fe74e24ce8d027333f8fedc9247a402d3683765983296",
        deprecated=True,
    )
    version(
        "4.3.1",
        sha256="88ada5f256a570792d1326a305663e94cf2c3b0cbd99f7e745326923882dafd2",
        deprecated=True,
    )
    version(
        "4.3.0",
        sha256="c3d9f408df8d4dc0e9c0026217b8c684f68e775da80b215fecb3cd24419ee6d3",
        deprecated=True,
    )
    version(
        "4.2.0",
        sha256="62a9c0cb1ba50b1c39a0636c886ac86e75a1a71cbf5fec05801517ceb0e67a37",
        deprecated=True,
    )
    version(
        "4.1.0",
        sha256="5d93de4e92895b6eb5f9d098f5dbd182d33923bd9b2ab69cf5a1abbf91d70695",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="f47859a46173228b597c463eda850b870e810534af5efd5f2a746067ef04edee",
        deprecated=True,
    )
    version(
        "3.10.0",
        sha256="ac4a1d059fc34377e906071fd0e56f5434a7e0e4ded9db8faf9217a115239dec",
        deprecated=True,
    )
    version(
        "3.9.0",
        sha256="0678f9faf45058b16923948c66d77ba2c072283c975d167899caef969169b292",
        deprecated=True,
    )
    version(
        "3.8.0",
        sha256="5154a84ce7568cd5dba756e9508c34ae9fc62f4b0b5731f93c2ad68b21537ed1",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="6fa5b771e990f09c242237ab334b9f01039ec7d54ccde993e719c5d6577d1518",
        deprecated=True,
    )
    version(
        "3.5.0",
        sha256="7af5326c9ca695642b4265232ec12864a61fd6b6056aa7c4ecd9e19c817f209e",
        deprecated=True,
    )

    def install(self, spec, prefix):
        source_directory = self.stage.source_path
        include = join_path(source_directory, "inc")

        def only_headers(p):
            return p.endswith("CMakeLists.txt") or p.endswith("RPM") or p.endswith("DEBIAN")

        mkdirp(prefix.roctracer.include)
        install_tree(include, prefix.roctracer.include, ignore=only_headers)
