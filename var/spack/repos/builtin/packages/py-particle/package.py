# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParticle(PythonPackage):
    """Particle provides a pythonic interface to the Particle Data Group (PDG)
    particle data tables and particle identification codes, with extended
    particle information and extra goodies."""

    git = "https://github.com/scikit-hep/particle.git"
    pypi = "particle/particle-0.11.0.tar.gz"
    homepage = "https://github.com/scikit-hep/particle"

    maintainers("vvolkl")

    tags = ["hep"]

    license("BSD-3-Clause")

    version(
        "0.23.0",
        sha256="d3734768b3dbcc40b3d6457266f87204ce61f6fdad0c8be2c0f6ced74208a46d",
        url="https://pypi.org/packages/06/b0/69334d12d8680705cf35d7ca7b4e8e7805e3ba9ca3dd8b846d6a1db8dda5/particle-0.23.0-py3-none-any.whl",
    )
    version(
        "0.22.1",
        sha256="9fce7d549d59a2f477103f1046360b1de093d0378b1c3046b0234e0abee52fa7",
        url="https://pypi.org/packages/c0/ec/e97d3ba0fea0b7277187225d7ba03ae0f0d16848ab7f2d72d064beb240cc/particle-0.22.1-py3-none-any.whl",
    )
    version(
        "0.22.0",
        sha256="b2bb8b4579372c5a8f5340dd98b72a1f95dfa3a41d41c3cd98ec2549370d474a",
        url="https://pypi.org/packages/c1/1b/caaa7616203082858e4bee9e1c8612896d506e162b59c2c57a727b88ad44/particle-0.22.0-py3-none-any.whl",
    )
    version(
        "0.21.2",
        sha256="b85aa51b4e993e58f672c61d8e43d03f0b45f072751868ec2f88f4f1d58c0e18",
        url="https://pypi.org/packages/4f/cc/26e051e887516456acbf6023aaa3314d80831834e25b5b9bb1e962ba0fa1/particle-0.21.2-py3-none-any.whl",
    )
    version(
        "0.21.1",
        sha256="840a130b5621471a4232bea0eec23b9942f1cbd53e159b65a025547a2cf9a024",
        url="https://pypi.org/packages/bd/3c/4038bd34eacc79944d3e8ab4fc9aecf7f6c15e7341edccbeb86cc7ac95bd/particle-0.21.1-py3-none-any.whl",
    )
    version(
        "0.21.0",
        sha256="d72b5b5915d62fa0a6cad9e17d8c062a9a6b9461de29ace5185b2b85124f85bb",
        url="https://pypi.org/packages/d7/7e/6951a1a874116727984e76ed1fe5da5af35cb3bf8d8b571f9fb8354e63ea/particle-0.21.0-py3-none-any.whl",
    )
    version(
        "0.20.1",
        sha256="06454cf92c87f973864b0b4bebe4a74cf0f3531d10abeb9e94a0d1b5ea88d9d4",
        url="https://pypi.org/packages/65/fa/5381aedb2138d076806537661cc14a02635961cf1d87bdc408b699c075d2/particle-0.20.1-py3-none-any.whl",
    )
    version(
        "0.20.0",
        sha256="f776526999331ce11f669e7861deb51a77c8bb63c46b075601f7ae2628e7fce6",
        url="https://pypi.org/packages/4e/60/98ce767618f91671dc0c0c09a57d1e53e06f60e0fa63769f7cd2e28469ef/particle-0.20.0-py2.py3-none-any.whl",
    )
    version(
        "0.16.3",
        sha256="4c406ec2a78d91b90b381a8e86b2ba43b1e17dcff6b1d55ddd466d1aebb89111",
        url="https://pypi.org/packages/25/d3/1b473898dcd8e3975f2154087b51186af6f5a6c98506420093baeaf058b8/particle-0.16.3-py2.py3-none-any.whl",
    )
    version(
        "0.16.2",
        sha256="5ecfc1fe5237f6fbf30d5cc150b3fc07b5e37300f2386db74b69bd46b1ab4569",
        url="https://pypi.org/packages/ee/6f/89ab9650e780557e9932c520ed721e73ea18857a187ed81402a73478e3d9/particle-0.16.2-py2.py3-none-any.whl",
    )
    version(
        "0.16.1",
        sha256="455a3fc22235cb2e2c4975c233c0f80606180a8aa490b4819a83b0a40769dc7c",
        url="https://pypi.org/packages/98/6f/bbf5e8b5c2c071d0458896a98c091b683b619b68dcb1bc4c42a21ee1fb73/particle-0.16.1-py2.py3-none-any.whl",
    )
    version(
        "0.16.0",
        sha256="b7d3cb7a00a43fbe2a9a91fe554841144d4fa4005cd9c2f59ea17281a4ccd5f9",
        url="https://pypi.org/packages/12/d0/c31aeebbe5ca9740d0d2ab55eb463dae8daf4b0f43542c7e78ef5b3a82eb/particle-0.16.0-py2.py3-none-any.whl",
    )
    version(
        "0.15.1",
        sha256="4029e9d2d4517d61325140687bff1a7f887e33c79994b12b2ad04f781a26f5eb",
        url="https://pypi.org/packages/3b/5a/721b23aee3573703b358246448a07c463019c6b8cc9391c0d6941d2713d5/particle-0.15.1-py2.py3-none-any.whl",
    )
    version(
        "0.14.1",
        sha256="d12ffd3cfcb0b662046013f4ac67dfb719c297c6c8c6fc25a9c6672a23faf674",
        url="https://pypi.org/packages/ff/4b/645684fd2511f685b2116fb1df98175532ed27b47b89d28a3bd3bc9c5585/particle-0.14.1-py2.py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="23472cb842c6509dd1b17920b069081bb455449a1d2c074b10c172fe6c3363b4",
        url="https://pypi.org/packages/d9/a4/893f995c981c107c76df952b4e5eaf61e9d7f24d38088978e0131174db81/particle-0.11.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.21:")
        depends_on("py-attrs@19.2:", when="@0.10:")
        depends_on("py-deprecated", when="@0.16:0.20.0,0.22:0.23.0")
        depends_on("py-hepunits@2:", when="@0.13:")
        depends_on("py-hepunits@1.2:", when="@0.10:0.12")
        depends_on("py-importlib-resources@2:", when="@0.16: ^python@:3.8")
        depends_on("py-importlib-resources@1:", when="@:0.15 ^python@:3.6")
        depends_on("py-typing-extensions", when="@0.16:0.23.0 ^python@:3.7")
