# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFlowcept(PythonPackage):
    """Capture and query workflow provenance data using data observability."""

    homepage = "https://github.com/ORNL/flowcept"
    pypi = "flowcept/flowcept-0.6.11.tar.gz"

    maintainers("renan-souza", "mdorier")

    license("MIT", checked_by="mdorier")

    version("0.8.1", sha256="3eb8b42a61a7ca5366df34fc59051a11b7df630cbf43a6a58363716953074d91")
    version("0.7.22", sha256="1c4c289d59225fd0dfb7f909b754a126112bbdcf3f4c9a401cc05c1c59ffd492")
    version("0.7.21", sha256="f03f9c0afaa53819907c3ad52a38aaf06d6bd015e5615379c0260a5b9bdbad81")
    version("0.7.20", sha256="f23df8b5b3f50028a3d85ca6893039633470144ae135748370a149312ce3ada6")
    version("0.7.19", sha256="9a41c85d1e15387f78e148a1b533a3ff25600f31ccd0774a090c85bf010ba945")
    version("0.7.18", sha256="bfc40f5336efb7f0857a95b9a45b7f3dcb9d96e3ad27bffb9336f4c2c6b971ec")
    version("0.7.17", sha256="fb627817489552fdcf48310ca842ffa463edeed07906ae9359b0166b69acff1a")
    version("0.7.16", sha256="46d0f0da24f61090ac0ad939fdc8bb61504c140464e8d269f947549394c86243")
    version("0.7.15", sha256="4d25764ddeb0a128f00bf8728af95e9c7ba0fb8554968e4a6c877807bb0557c1")
    version("0.7.14", sha256="eea9cf2b3c938796e3d3c987ef458ad118671e67f5638b1b71cb4bceacc36cc0")
    version("0.7.13", sha256="d9aa3d93f5dcb618e2509f86ea818f23ff20fe65cb647c05cfa56facb71731c4")
    version("0.7.12", sha256="2b3b337c7e976fab26be8752b254ce3b35d951e959eb92b8720a93e692c9330e")
    version("0.7.11", sha256="3f97b746a75a6c7c74dd1045ff14805f59473a9a8691e68c50c359e1f06d6c0e")
    version("0.7.10", sha256="57f308ab1b155bc7591b59a6e43b5a830c8adfe35e35d1f5dc6f1f57a06a5874")
    version("0.7.9", sha256="86753568dd10f8b7e8630fbdd1b7647d6b648b1f158583be616382f762c08ae5")
    version("0.7.8", sha256="266efc6fd20c16b80f713c1ebbb4834a59746442a9ef78b4d656ca7fda30c476")
    version("0.7.7", sha256="e430116c51a3777ca64cf1614998fac5e824f6739af8aa0f8167ee84ece577cf")
    version("0.7.6", sha256="587d22a6d8c5f4777b5cb72bff275ce4d913bf56eaa80596f52059f53196fd55")
    version("0.7.5", sha256="6182a78be818e15b63bf45c6cbeead1fc1f9755c985b194622d8d8acf211da1d")
    version("0.7.4", sha256="777ba1e70fa7f7df725ec5481364e3d17ab5613c41031d03dac7985ba08b0955")
    version("0.7.3", sha256="ec772fbe29627c143c4f21fd97bb37497b99764c9e584818e359d794879ff11e")
    version("0.7.2", sha256="ccf13e3976bf9a10cac1b035d86242303eb9eeb4a7e5dbda29ae3719d82aa0ee")
    version("0.7.1", sha256="0b41a35aaac2a321968f2e645c73175cbd42bc68cc798268c21cf45400f9e776")
    version("0.6.14", sha256="83fde706ac7378c5494b1805803c1f59e767492f689224eb29ca777c51285b2a")
    version("0.6.13", sha256="e9f8ef5340325b6118dc844d0d7beb6b5944f41ccd410eaca12facb5fad6db42")
    version("0.6.12", sha256="3f79430c024fd9fef6a222739587f243d5a0e8d89d43decda637e098fc3ea90c")
    version("0.6.11", sha256="3a87c5f6835410a34b158efc9ab21ba686af26b609cff8beebc53bfb2a20c3dc")

    variant("kafka", default=False, description="Replace Redis with Kafka")
    variant("dask", default=False, description="Enable Dask support")

    depends_on("py-hatchling", type="build")
    with default_args(type=("build", "run")):
        depends_on("py-flask-restful")
        depends_on("py-msgpack")
        depends_on("py-omegaconf")
        depends_on("py-pandas")
        depends_on("py-psutil@6.1.1:")
        depends_on("py-py-cpuinfo")
        depends_on("py-pymongo", when="@:0.6.14")
        depends_on("py-redis")
        depends_on("py-requests")
        depends_on("py-confluent-kafka@:2.8.0", when="+kafka")
        depends_on("py-tomli", when="+dask")
        depends_on("py-dask@:2024.10.0+distributed", when="+dask")
        depends_on("py-arrow", when="@0.7.4:")
        depends_on("py-lmdb", when="@0.7.1:")
