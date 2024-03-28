# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorboard(PythonPackage):
    """TensorBoard is a suite of web applications for inspecting and understanding
    your TensorFlow runs and graphs."""

    homepage = "https://github.com/tensorflow/tensorboard"
    url = "https://files.pythonhosted.org/packages/py3/t/tensorboard/tensorboard-2.9.1-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tensorboard/"

    # Requires tensorflow
    skip_modules = ["tensorboard.summary._tf"]

    maintainers("aweits")

    license("Apache-2.0")

    version(
        "2.16.2",
        sha256="9f2b4e7dad86667615c0e5cd072f1ea8403fc032a299f0072d6f74855775cc45",
        url="https://pypi.org/packages/3a/d0/b97889ffa769e2d1fdebb632084d5e8b53fc299d43a537acee7ec0c021a3/tensorboard-2.16.2-py3-none-any.whl",
    )
    version(
        "2.16.1",
        sha256="928b62567911a8eeb2ebeb7482a9e4599b35f6713a6f2c56655259c18a139569",
        url="https://pypi.org/packages/47/0b/4a77524dea22ecae8934d4ff968d7700c66db9cca898799ccc7bb548ccdf/tensorboard-2.16.1-py3-none-any.whl",
    )
    version(
        "2.16.0",
        sha256="263b909a2009cb3a79daa6abe64c1785cc317c25a54e4db2fecb6429ffc54c58",
        url="https://pypi.org/packages/92/15/57b5ea84096173214554c5b0c5a7528ff194c2357cc75fed12cf0ee1bc55/tensorboard-2.16.0-py3-none-any.whl",
    )
    version(
        "2.15.2",
        sha256="a6f6443728064d962caea6d34653e220e34ef8df764cb06a8212c17e1a8f0622",
        url="https://pypi.org/packages/37/12/f6e9b9dcc310263cbd3948274e286538bd6800fd0c268850788f14a0c6d0/tensorboard-2.15.2-py3-none-any.whl",
    )
    version(
        "2.15.1",
        sha256="c46c1d1cf13a458c429868a78b2531d8ff5f682058d69ec0840b0bc7a38f1c0f",
        url="https://pypi.org/packages/6e/0c/1059a6682cf2cc1fcc0d5327837b5672fe4f5574255fa5430d0a8ceb75e9/tensorboard-2.15.1-py3-none-any.whl",
    )
    version(
        "2.15.0",
        sha256="c05b4d02a3a9fd4bd6c25265087d52b49b790a871ddf98f4fb32fe97cbbc7ad0",
        url="https://pypi.org/packages/69/38/fb2ac9c4c8efbe020ae88f6772be87d51ef18526ac541fc3393786b7c45a/tensorboard-2.15.0-py3-none-any.whl",
    )
    version(
        "2.14.1",
        sha256="3db108fb58f023b6439880e177743c5f1e703e9eeb5fb7d597871f949f85fd58",
        url="https://pypi.org/packages/73/a2/66ed644f6ed1562e0285fcd959af17670ea313c8f331c46f79ee77187eb9/tensorboard-2.14.1-py3-none-any.whl",
    )
    version(
        "2.14.0",
        sha256="3667f9745d99280836ad673022362c840f60ed8fefd5a3e30bf071f5a8fd0017",
        url="https://pypi.org/packages/bc/a2/ff5f4c299eb37c95299a76015da3f30211468e29d8d6f1d011683279baee/tensorboard-2.14.0-py3-none-any.whl",
    )
    version(
        "2.13.0",
        sha256="ab69961ebddbddc83f5fa2ff9233572bdad5b883778c35e4fe94bf1798bd8481",
        url="https://pypi.org/packages/67/f2/e8be5599634ff063fa2c59b7b51636815909d5140a26df9f02ce5d99b81a/tensorboard-2.13.0-py3-none-any.whl",
    )
    version(
        "2.12.3",
        sha256="b4a69366784bc347e02fbe7d847e01896a649ca52f8948a11005e205dcf724fb",
        url="https://pypi.org/packages/32/09/86e2ef3b4f4ec04bde0eca499325f291ae6b3313381d0666ee20b5b80c73/tensorboard-2.12.3-py3-none-any.whl",
    )
    version(
        "2.12.2",
        sha256="811ab0d27a139445836db9fd4f974424602c3dce12379364d379bcba7c783a68",
        url="https://pypi.org/packages/aa/80/f7233129f75d0d1b35e67df3a48010fffd21ccde124847e3c33d503fef01/tensorboard-2.12.2-py3-none-any.whl",
    )
    version(
        "2.12.1",
        sha256="58f1c2a25b4829b9c48d2b1ec951dedc9325dcd1ea4b0f601d241d2887d0ed65",
        url="https://pypi.org/packages/93/f4/59b871fbdb2f52ba50ae234e3e5617208f99a053157c37fc0ce9cd46c40b/tensorboard-2.12.1-py3-none-any.whl",
    )
    version(
        "2.12.0",
        sha256="3cbdc32448d7a28dc1bf0b1754760c08b8e0e2e37c451027ebd5ff4896613012",
        url="https://pypi.org/packages/8d/71/75fcfab1ff98e3fad240f760d3a6b5ca6bdbcc5ed141fb7abd35cf63134c/tensorboard-2.12.0-py3-none-any.whl",
    )
    version(
        "2.11.2",
        sha256="cbaa2210c375f3af1509f8571360a19ccc3ded1d9641533414874b5deca47e89",
        url="https://pypi.org/packages/6f/77/e624b4916531721e674aa105151ffa5223fb224d3ca4bd5c10574664f944/tensorboard-2.11.2-py3-none-any.whl",
    )
    version(
        "2.11.1",
        sha256="0c7529f3f43691e8cc2ece8e564c2e103c51ade317c6af626d415239b5088018",
        url="https://pypi.org/packages/70/6a/95cedf185fa0063d4a6d8251b5601071e58a4ef15202dbf93773f13c7383/tensorboard-2.11.1-py3-none-any.whl",
    )
    version(
        "2.11.0",
        sha256="a0e592ee87962e17af3f0dce7faae3fbbd239030159e9e625cce810b7e35c53d",
        url="https://pypi.org/packages/05/70/ee7968f4a92ff9f95354d0ccaa9c0ba17b2644a33472ea845d92dd4e4821/tensorboard-2.11.0-py3-none-any.whl",
    )
    version(
        "2.10.1",
        sha256="fb9222c1750e2fa35ef170d998a1e229f626eeced3004494a8849c88c15d8c1c",
        url="https://pypi.org/packages/80/49/a5ec29886ef823718c8ae54ed0b3ad7e19066b5bf21cec5038427e6a04c4/tensorboard-2.10.1-py3-none-any.whl",
    )
    version(
        "2.10.0",
        sha256="76c91a5e8959cd2208cc32cb17a0cb002badabb66a06ac2af02a7810f49a59e3",
        url="https://pypi.org/packages/6b/42/e271c40c84c250b52fa460fda970899407c837a2049c53969f37e404b1f6/tensorboard-2.10.0-py3-none-any.whl",
    )
    version(
        "2.9.1",
        sha256="baa727f791776f9e5841d347127720ceed4bbd59c36b40604b95fb2ae6029276",
        url="https://pypi.org/packages/ee/0d/23812e6ce63b3d87c39bc9fee83e28c499052fa83fddddd7daea21a6d620/tensorboard-2.9.1-py3-none-any.whl",
    )
    version(
        "2.9.0",
        sha256="bd78211076dca5efa27260afacfaa96cd05c7db12a6c09cc76a1d6b2987ca621",
        url="https://pypi.org/packages/69/80/a3abccc4ea941c36741751206e40e619afe28652cf76f74cfa4c3e4248ba/tensorboard-2.9.0-py3-none-any.whl",
    )
    version(
        "2.8.0",
        sha256="65a338e4424e9079f2604923bdbe301792adce2ace1be68da6b3ddf005170def",
        url="https://pypi.org/packages/f7/fd/67c61276de025801cfa8a1b9af2d7c577e7f27c17b6bff2baca20bf03543/tensorboard-2.8.0-py3-none-any.whl",
    )
    version(
        "2.7.0",
        sha256="239f78a4a8dff200ce585a030c787773a8c1184d5c159252f5f85bac4e3c3b38",
        url="https://pypi.org/packages/2d/eb/80f75ab480cfbd032442f06ec7c15ef88376c5ef7fd6f6bf2e0e03b47e31/tensorboard-2.7.0-py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="f7dac4cdfb52d14c9e3f74585ce2aaf8e6203620a864e51faf84988b09f7bbdb",
        url="https://pypi.org/packages/a0/20/a59a30c32330e4ff704faa4273b251db042d495e0c367bcdf045c6fe26e9/tensorboard-2.6.0-py3-none-any.whl",
    )
    version(
        "2.5.0",
        sha256="e167460085b6528956b33bab1c970c989cdce47a6616273880733f5e7bde452e",
        url="https://pypi.org/packages/44/f5/7feea02a3fb54d5db827ac4b822a7ba8933826b36de21880518250b8733a/tensorboard-2.5.0-py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="7b8c53c396069b618f6f276ec94fc45d17e3282d668979216e5d30be472115e4",
        url="https://pypi.org/packages/64/21/eebd23060763fedeefb78bc2b286e00fa1d8abda6f70efa2ee08c28af0d4/tensorboard-2.4.1-py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="cde0c663a85609441cb4d624e7255fd8e2b6b1d679645095aac8a234a2812738",
        url="https://pypi.org/packages/02/83/179c8f76e5716030cc3ee9433721161cfcc1d854e9ba20c9205180bb100a/tensorboard-2.4.0-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="d34609ed83ff01dd5b49ef81031cfc9c166bba0dabd60197024f14df5e8eae5e",
        url="https://pypi.org/packages/e9/1b/6a420d7e6ba431cf3d51b2a5bfa06a958c4141e3189385963dc7f6fbffb6/tensorboard-2.3.0-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="bb6bbc75ad2d8511ba6cbd49e4417276979f49866e11841e83da8298727dbaed",
        url="https://pypi.org/packages/54/f5/d75a6f7935e4a4870d85770bc9976b12e7024fbceb83a1a6bc50e6deb7c4/tensorboard-2.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@2.14.1:")
        depends_on("py-absl-py@0.4:", when="@1.13:")
        depends_on("py-google-auth@1.6.3:", when="@2.7:2.15")
        depends_on("py-google-auth@1.6.3:1", when="@2.0.1:2.6")
        depends_on("py-google-auth-oauthlib@0.5:", when="@2.15")
        depends_on("py-google-auth-oauthlib@0.5:1.0", when="@2.12.1:2.14")
        depends_on("py-google-auth-oauthlib@0.4.1:0.4", when="@2.0.1:2.12.0")
        depends_on("py-grpcio@1.48.2:", when="@2.12:")
        depends_on("py-grpcio@1.24.3:", when="@2.0.1:2.11")
        depends_on("py-markdown@2.6.8:")
        depends_on("py-numpy@1.12.0:")
        depends_on("py-protobuf@3.19.6:4.24.0-rc3,4.24.1:", when="@2.15.2:")
        depends_on("py-protobuf@3.19.6:4.23", when="@2.15:2.15.1")
        depends_on("py-protobuf@3.19.6:", when="@2.12:2.14")
        depends_on("py-protobuf@3.9.2:3", when="@2.11")
        depends_on("py-protobuf@3.9.2:3.19", when="@2.9.1:2.10")
        depends_on("py-protobuf@3.9.2:", when="@2.9:2.9.0")
        depends_on("py-protobuf@3.6:", when="@1.13:2.8")
        depends_on("py-requests@2.21:", when="@2.0.2:2.15")
        depends_on("py-setuptools@41:", when="@1.14:")
        depends_on("py-six@1.10:", when="@:2.4,2.14.1:")
        depends_on("py-tensorboard-data-server@0.7:", when="@2.12:")
        depends_on("py-tensorboard-data-server@0.6", when="@2.5:2.11")
        depends_on("py-tensorboard-plugin-wit", when="@2.2:2.12.2")
        depends_on("py-tf-keras@2.15.0:", when="@2.16.1")
        depends_on("py-tf-keras-nightly", when="@2.16:2.16.0")
        depends_on("py-werkzeug@1.0.1:", when="@2.9:")
        depends_on("py-werkzeug@0.11.15:", when="@1.13:2.8")
        depends_on("py-wheel@0.26:", when="@:2.14.0")

    # Historical dependencies
