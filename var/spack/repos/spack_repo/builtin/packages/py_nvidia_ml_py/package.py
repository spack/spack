# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyNvidiaMlPy(PythonPackage):
    """Python Bindings for the NVIDIA Management Library."""

    homepage = "https://www.nvidia.com/"
    pypi = "nvidia-ml-py/nvidia-ml-py-11.450.51.tar.gz"

    license("BSD-2-Clause")

    version("12.575.51", sha256="6490e93fea99eb4e966327ae18c6eec6256194c921f23459c8767aee28c54581")
    version("12.570.86", sha256="0508d4a0c7b6d015cf574530b95a62ed4fc89da3b8b47e1aefe6777db170ec8b")
    version("12.560.30", sha256="f0254dc7400647680a072ee02509bfd46102b60bdfeca321576d4d4817e7fe97")
    version("12.555.43", sha256="e9e7f12ef1ec234bb0dc22d2bdc762ffafab394bdc472a07a4377c95bbf93afe")
    version("12.550.89", sha256="02f299a341db7f938883c9a1098d28396dc29d5bb6b0f2806833e7dafff071f1")
    version(
        "12.535.161", sha256="2bcc31ff7a0ea291ed8d7fc39b149391a42c2fb1cb4256c935e692de488b4d17"
    )
    version(
        "11.525.150", sha256="50af55b99ea167781102345a7de29bac94a57c8f38de6757ef9f945dd137c90a"
    )
    version("11.515.75", sha256="e3c75f06d5a3201dc51136e00e58c5c132b3be5d604d86c143426adb4e41c490")
    version("11.510.69", sha256="f7e0cd3a266c7c88ae5467cc6b7dab13d26adfd6b8e4ec8c555a4cc9897ce907")
    version("11.495.46", sha256="8f68e1af274756067632c7e1b79fb1a93a8dddf1e04851fccaeb34adfa599625")
    version("11.470.66", sha256="20fff0dcd40b32fdc674cd98bc614bb8b6cc8d488687a55bf8c569eef39541f3")
    version("11.460.79", sha256="5b7c051cd55469848960bb9fde07dc8fd25d21853307eeba669bfe3c3ede11c5")
    version(
        "11.450.129", sha256="b0170a3f16efdd055c283d3b94c7d2d517f32456e84ad118d809396929fcad4f"
    )
    version("11.450.51", sha256="5aa6dd23a140b1ef2314eee5ca154a45397b03e68fd9ebc4f72005979f511c73")

    depends_on("py-setuptools", type="build")

    # pip silently replaces distutils with setuptools

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/n/nvidia-ml-py/nvidia{0}ml{0}py-{1}.tar.gz"
        if version > Version("12.560.30"):
            sep = "_"
        else:
            sep = "-"
        return url.format(sep, version)
