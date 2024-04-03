# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinx(PythonPackage):
    """Sphinx Documentation Generator."""

    homepage = "https://www.sphinx-doc.org/en/master/"
    pypi = "Sphinx/sphinx-7.1.0.tar.gz"

    maintainers("adamjstewart")

    license("BSD-2-Clause")

    version(
        "7.2.6",
        sha256="1e09160a40b956dc623c910118fa636da93bd3ca0b9876a7b3df90f07d691560",
        url="https://pypi.org/packages/b2/b6/8ed35256aa530a9d3da15d20bdc0ba888d5364441bb50a5a83ee7827affe/sphinx-7.2.6-py3-none-any.whl",
    )
    version(
        "7.2.5",
        sha256="9269f9ed2821c9ebd30e4204f5c2339f5d4980e377bc89cb2cb6f9b17409c20a",
        url="https://pypi.org/packages/a6/54/f4fcf7113eb051a46476ecce9485c463f58dbc3887c06dbfe1e67a8ce7c0/sphinx-7.2.5-py3-none-any.whl",
    )
    version(
        "7.2.4",
        sha256="9b3aa23254ffc5be468646810543e491653bf5a67f3f23e4ccd4e515b0bd0b9c",
        url="https://pypi.org/packages/12/68/eac1b2f976569d5323306d4ad9668d181fc5b78456f5ce5d1eb152c632dd/sphinx-7.2.4-py3-none-any.whl",
    )
    version(
        "7.2.3",
        sha256="6379ea22c49955a44ed4e62bde8c94575e9544303cc0554eaa97099ae5853a3a",
        url="https://pypi.org/packages/3b/4e/5827d0be7c4596e64c03b6c544287ee97c13c0bbbe872f5f1e551b29b67b/sphinx-7.2.3-py3-none-any.whl",
    )
    version(
        "7.2.2",
        sha256="ed33bc597dd8f05cd37118f64cbac0b8bf773389a628ddfe95ab9e915c9308dc",
        url="https://pypi.org/packages/40/c0/e62ce9d243bfa2d9f290d7c730c7df3d9e979f0016e38c767f33ffcc2185/sphinx-7.2.2-py3-none-any.whl",
    )
    version(
        "7.2.1",
        sha256="332ac9be5c7b61d72f8e7303bae88cb5dc82a9ba378d77275539394d46ff5b7a",
        url="https://pypi.org/packages/e8/9e/1c58852aa27a9e032bb193295ee0f97a308d259b60dcce57b8ab1d49c45b/sphinx-7.2.1-py3-none-any.whl",
    )
    version(
        "7.2.0",
        sha256="93f235913abd52a4544e14457880d4964b2b8efa40eadad445816cd2449842df",
        url="https://pypi.org/packages/13/3a/a2fb7b66f3f0f4cde560bd33624aec0f4a4d003225cec17cf77c79a235ce/sphinx-7.2.0-py3-none-any.whl",
    )
    version(
        "7.1.2",
        sha256="d170a81825b2fcacb6dfd5a0d7f578a053e45d3f2b153fecc948c37344eb4cbe",
        url="https://pypi.org/packages/48/17/325cf6a257d84751a48ae90752b3d8fe0be8f9535b6253add61c49d0d9bc/sphinx-7.1.2-py3-none-any.whl",
    )
    version(
        "7.1.1",
        sha256="4e6c5ea477afa0fb90815210fd1312012e1d7542589ab251ac9b53b7c0751bce",
        url="https://pypi.org/packages/c7/64/c3d5a265ebc2e96a6d1c1b3f5d23abdd3dde547d8638a4d06383aa8d2059/sphinx-7.1.1-py3-none-any.whl",
    )
    version(
        "7.1.0",
        sha256="9bdfb5a2b28351d4fdf40a63cd006dbad727f793b243e669fc950d7116c634af",
        url="https://pypi.org/packages/c6/33/1cb96d522c5b09080d41c6e23fc4f6bc88d964751fa331786e9ab59b6eca/sphinx-7.1.0-py3-none-any.whl",
    )
    version(
        "7.0.1",
        sha256="60c5e04756c1709a98845ed27a2eed7a556af3993afb66e77fec48189f742616",
        url="https://pypi.org/packages/4b/a9/9760e8373a11a62f5ef66684771b0a5b2c4a699bf0dbbc650ca2b75cec36/sphinx-7.0.1-py3-none-any.whl",
    )
    version(
        "7.0.0",
        sha256="3cfc1c6756ef1b132687b813ec6ea2214cb7a7e5d1dcb2772006cb895a0fa469",
        url="https://pypi.org/packages/ee/0e/2c819414c8dad75c55f7ced4044ac48c6fcce8b7a2614bad12612aa4b1ac/sphinx-7.0.0-py3-none-any.whl",
    )
    version(
        "6.2.1",
        sha256="97787ff1fa3256a3eef9eda523a63dbf299f7b47e053cfcf684a1c2a8380c912",
        url="https://pypi.org/packages/5f/d8/45ba6097c39ba44d9f0e1462fb232e13ca4ddb5aea93a385dcfa964687da/sphinx-6.2.1-py3-none-any.whl",
    )
    version(
        "6.2.0",
        sha256="ff1c2a1167bef9cdcd8ec71339e85fe10f26d4e9ef9382ef10b2687c876c936b",
        url="https://pypi.org/packages/82/7b/880b3d63fe87f9084644c1ed11113ae5775f13df0d417447e96c4c604bab/sphinx-6.2.0-py3-none-any.whl",
    )
    version(
        "6.1.3",
        sha256="807d1cb3d6be87eb78a381c3e70ebd8d346b9a25f3753e9947e866b2786865fc",
        url="https://pypi.org/packages/2e/2c/22a20486cad91a66f4f70bd88c20c8bb306ae719cbba93d7debae7efa80d/sphinx-6.1.3-py3-none-any.whl",
    )
    version(
        "6.1.2",
        sha256="2add7555f702f3e70654e04ac352d14974c8deb4a1e0785860914cd1269688f9",
        url="https://pypi.org/packages/89/ea/7ca493912693b1a46420cba13be885b3a1d758990c72f5d2b51916ce092f/sphinx-6.1.2-py3-none-any.whl",
    )
    version(
        "6.1.1",
        sha256="5818c36a250f60d2767f2cee14247b7f39882d97f582e3696958000b65665c5b",
        url="https://pypi.org/packages/9c/53/2ad8a7dd5a6a0f036fc28bc045056bbadc892fdbd888b0f949cdff721acb/sphinx-6.1.1-py3-none-any.whl",
    )
    version(
        "6.1.0",
        sha256="7569d01418166c079560751038ab1c0ddca3b15c74787cc60b16d7f11a4bf35a",
        url="https://pypi.org/packages/5e/dd/1bb2e6dbdcb4ab4eba960a0073c164a0239e3b2cab191ca25a9eefa7e9e7/sphinx-6.1.0-py3-none-any.whl",
    )
    version(
        "6.0.1",
        sha256="4ad5caa630835a794ee4f6f4772300f407b7d6ac05b418abfb5c7c38f9b24d18",
        url="https://pypi.org/packages/1d/a7/45135386be5609225fee4c58a92a8cd891ecc67c4314b6c7a883bf0cda85/sphinx-6.0.1-py3-none-any.whl",
    )
    version(
        "6.0.0",
        sha256="c2aeebfcb0e7474f5a820eac6177c7492b1d3c9c535aa21d5ae77cab2f3600e4",
        url="https://pypi.org/packages/d4/a3/83304f734ba5b5b400af0de3d31d1844ea295c1652435668c9aa2b8650c0/sphinx-6.0.0-py3-none-any.whl",
    )
    version(
        "5.3.0",
        sha256="060ca5c9f7ba57a08a1219e547b269fadf125ae25b06b9fa7f66768efb652d6d",
        url="https://pypi.org/packages/67/a7/01dd6fd9653c056258d65032aa09a615b5d7b07dd840845a9f41a8860fbc/sphinx-5.3.0-py3-none-any.whl",
    )
    version(
        "5.2.3",
        sha256="7abf6fabd7b58d0727b7317d5e2650ef68765bbe0ccb63c8795fa8683477eaa2",
        url="https://pypi.org/packages/27/55/9799046be6e9a02ff1955d74dffa2b096a2fe204d1004a8499d6953d62d2/sphinx-5.2.3-py3-none-any.whl",
    )
    version(
        "5.2.2",
        sha256="9150a8ed2e98d70e778624373f183c5498bf429dd605cf7b63e80e2a166c35a5",
        url="https://pypi.org/packages/f0/e5/aa7a7622cb708c0525c473a52ade07e078a9241092c32705e941d4d6878e/sphinx-5.2.2-py3-none-any.whl",
    )
    version(
        "5.2.1",
        sha256="3dcf00fcf82cf91118db9b7177edea4fc01998976f893928d0ab0c58c54be2ca",
        url="https://pypi.org/packages/00/5c/27480aeb398ab549cbb0840d154464d4854ac49f6fff0b452e106bc54f8e/sphinx-5.2.1-py3-none-any.whl",
    )
    version(
        "5.2.0",
        sha256="422812bdf2dacab55c47ee4dd4746bb82e739fe4c97ce16dd68bcc208e348e73",
        url="https://pypi.org/packages/41/ba/0ba25864b6ab4101d052b76150d658fdd057d4d73dd19609953ad167f1ca/sphinx-5.2.0-py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="309a8da80cb6da9f4713438e5b55861877d5d7976b69d87e336733637ea12693",
        url="https://pypi.org/packages/83/74/318d8cd70cbde2164e3035f9e9ba0807e2de7d384e03784ad0afc98b891b/Sphinx-5.1.1-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="50661b4dbe6a4a1ac15692a7b6db48671da6bae1d4d507e814f1b8525b6bba86",
        url="https://pypi.org/packages/63/2c/428ba829110a52ef0881c22f031aa943367b1739f853df3b4976090e1c29/Sphinx-5.1.0-py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="d3e57663eed1d7c5c50895d191fdeda0b54ded6f44d5621b50709466c338d1e8",
        url="https://pypi.org/packages/fd/a2/3139e82a7caa2fb6954d0e63db206cc60e0ad6c67ae61ef9cf87dc70ade1/Sphinx-5.0.2-py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="36aa2a3c2f6d5230be94585bc5d74badd5f9ed8f3388b8eedc1726fe45b1ad30",
        url="https://pypi.org/packages/5a/bc/7c06c6c68a85e57a7ea5b3274c1adc221591addb164b5136009fb0fee8f4/Sphinx-5.0.1-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="af248b21e3282f847ff20feebe7a1985fb34773cbe3fc75bf206897f1a2199c4",
        url="https://pypi.org/packages/68/24/4ea9d6189a5b2db45adf12aafbaa5b489910b3a4f106a0ea7ecdcf70dae0/Sphinx-5.0.0-py3-none-any.whl",
    )
    version(
        "4.5.0",
        sha256="ebf612653238bcc8f4359627a9b7ce44ede6fdd75d9d30f68255c7383d3a6226",
        url="https://pypi.org/packages/91/96/9cbbc7103fb482d5809fe4976ecb9b627058210d02817fcbfeebeaa8f762/Sphinx-4.5.0-py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="5da895959511473857b6d0200f56865ed62c31e8f82dd338063b84ec022701fe",
        url="https://pypi.org/packages/c4/85/978c06c898331b72080242f18ab7a6021f1055285fb1db9e6554c79264cd/Sphinx-4.4.0-py3-none-any.whl",
    )
    version(
        "4.3.2",
        sha256="6a11ea5dd0bdb197f9c2abc2e0ce73e01340464feaece525e64036546d24c851",
        url="https://pypi.org/packages/30/30/065cac95f6b55edf93756b5478a416b4d727480e901e94c2575e9ea38d99/Sphinx-4.3.2-py3-none-any.whl",
    )
    version(
        "4.3.1",
        sha256="048dac56039a5713f47a554589dc98a442b39226a2b9ed7f82797fcb2fe9253f",
        url="https://pypi.org/packages/3a/05/8473b0d9b8e502b0d64c2383a60643525f691a98479707c385915cffb225/Sphinx-4.3.1-py3-none-any.whl",
    )
    version(
        "4.3.0",
        sha256="7e2b30da5f39170efcd95c6270f07669d623c276521fee27ad6c380f49d2bf5b",
        url="https://pypi.org/packages/5c/13/bcd209786eb4039a27514df74b344ba313bf20b9c56d39f489fc58789b95/Sphinx-4.3.0-py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="98a535c62a4fcfcc362528592f69b26f7caec587d32cd55688db580be0287ae0",
        url="https://pypi.org/packages/00/08/c037fa5d3794729fdc7967e5a174642c8e94e1988ae2bc950515e2902ca2/Sphinx-4.2.0-py3-none-any.whl",
    )
    version(
        "4.1.2",
        sha256="46d52c6cee13fec44744b8c01ed692c18a640f6910a725cbb938bc36e8d64544",
        url="https://pypi.org/packages/11/75/86ea47591cd6f8e1dc0d795f65799025f368f7a4647ce9a43320a62374d8/Sphinx-4.1.2-py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="3d513088236eef51e5b0adb78b0492eb22cc3b8ccdb0b36dd021173b365d4454",
        url="https://pypi.org/packages/e0/a1/0b983f8c23ca0eeb8573414ea9f0b6e0182b2a2e688a60c05b5a168158da/Sphinx-4.1.1-py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="51028bb0d3340eb80bcc1a2d614e8308ac78d226e6b796943daf57920abc1aea",
        url="https://pypi.org/packages/e0/c2/b76e4faab7d06a428fe0980e69a8cd09a62c7d9560140f4fc3225f7b9cd1/Sphinx-4.1.0-py3-none-any.whl",
    )
    version(
        "4.0.3",
        sha256="5747f3c855028076fcff1e4df5e75e07c836f0ac11f7df886747231092cfe4ad",
        url="https://pypi.org/packages/31/bb/591a6950bbbf65d6845f5eb24fb5a07d2441736723c68dbd35adaec34781/Sphinx-4.0.3-py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="d1cb10bee9c4231f1700ec2e24a91be3f3a3aba066ea4ca9f3bbe47e59d5a1d4",
        url="https://pypi.org/packages/6e/8b/6662db1f132fc32e9ad10e2441a17b7d67219d7394b570434bee8b420301/Sphinx-4.0.2-py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="b2566f5f339737a6ef37198c47d56de1f4a746c722bebdb2fe045c34bfd8b9d0",
        url="https://pypi.org/packages/a7/5b/50ccdef4683ffac13fdf4cc80fa9ced84849fd4eca444dec22e6c937a1e2/Sphinx-4.0.1-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="904e02cd0f84bed5d3748358c228ae3df3ad725b9e6cdc2166e17b309ed2e1fa",
        url="https://pypi.org/packages/5d/dc/54f8aec1d630a04b459f6dd19fa4590b28bf732c5201186941d93181c5d7/Sphinx-4.0.0-py3-none-any.whl",
    )
    version(
        "3.5.4",
        sha256="2320d4e994a191f4b4be27da514e46b3d6b420f2ff895d064f52415d342461e8",
        url="https://pypi.org/packages/a3/e7/9af5e0766e801cf0ad64eedab70dcea17646c3a0d309980b25426ccc53ec/Sphinx-3.5.4-py3-none-any.whl",
    )
    version(
        "3.4.1",
        sha256="aeef652b14629431c82d3fe994ce39ead65b3fe87cf41b9a3714168ff8b83376",
        url="https://pypi.org/packages/6d/b6/020cd8e0706bed5fce458017b002099ba4a3564e5a35788bc2607842435a/Sphinx-3.4.1-py3-none-any.whl",
    )
    version(
        "3.2.0",
        sha256="f7db5b76c42c8b5ef31853c2de7178ef378b985d7793829ec071e120dac1d0ca",
        url="https://pypi.org/packages/98/66/794a02ad5fdb844f494ed1fe18af5d2a29a26fe0b57c8d52c5c4fa8312b7/Sphinx-3.2.0-py3-none-any.whl",
    )
    version(
        "3.0.0",
        sha256="b63a0c879c4ff9a4dffcb05217fa55672ce07abdeb81e33c73303a563f8d8901",
        url="https://pypi.org/packages/d1/8e/89eabf81ae9ecc988743a5a989ca53d64558b4ed78f50698257173541ce0/Sphinx-3.0.0-py3-none-any.whl",
    )
    version(
        "2.4.4",
        sha256="fc312670b56cb54920d6cc2ced455a22a547910de10b3142276495ced49231cb",
        url="https://pypi.org/packages/16/c1/1c8016475cb612a64ce613c6b61c16224fe6dcfd9527792016ce611c231c/Sphinx-2.4.4-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="839a3ed6f6b092bb60f492024489cc9e6991360fb9f52ed6361acd510d261069",
        url="https://pypi.org/packages/8e/4c/95a21788db2e1653e931420f561015a0bbc9bd4660c4520467ab9e733eb2/Sphinx-2.2.0-py3-none-any.whl",
    )
    version(
        "1.8.5",
        sha256="9f3e17c64b34afc653d7c5ec95766e03043cc6d80b0de224f59b6b6e19d37c3c",
        url="https://pypi.org/packages/7d/66/a4af242b4348b729b9d46ce5db23943ce9bca7da9bbe2ece60dc27f26420/Sphinx-1.8.5-py2.py3-none-any.whl",
    )
    version(
        "1.8.4",
        sha256="b53904fa7cb4b06a39409a492b949193a1b68cc7241a1a8ce9974f86f0d24287",
        url="https://pypi.org/packages/75/25/905f901fb749e45cb201f1d946e82f59d84730c430287ea7980b0bcbd2dc/Sphinx-1.8.4-py2.py3-none-any.whl",
    )
    version(
        "1.8.2",
        sha256="b348790776490894e0424101af9c8413f2a86831524bd55c5f379d3e3e12ca64",
        url="https://pypi.org/packages/ff/d5/3a8727d6f890b1ae45da72a55bf8449e9f2c535a444923b338c3f509f203/Sphinx-1.8.2-py2.py3-none-any.whl",
    )
    version(
        "1.7.4",
        sha256="2e7ad92e96eff1b2006cf9f0cdb2743dacbae63755458594e9e8238b0c3dc60b",
        url="https://pypi.org/packages/89/44/73cd04b856fa35a69e9e2e790aa283e2eaefb684e116f1d46d01a5e7986f/Sphinx-1.7.4-py2.py3-none-any.whl",
    )
    version(
        "1.6.3",
        sha256="3ea0faf3e152a0e40372d8495c8cbd59e93f89266231c367d8098ec0dfede98f",
        url="https://pypi.org/packages/2d/96/97bebe9e13284fac32b6712ddf1dab5441f649ef24343ebfec98ba017553/Sphinx-1.6.3-py2.py3-none-any.whl",
    )
    version(
        "1.6.1",
        sha256="50974b1405f0d2a452013283b7d3ff20305b4bd8ecb65566c6f9f6192b7625a0",
        url="https://pypi.org/packages/57/61/991b604fe8e928a94afc3fd20d515f473b6969670233c92c0ad81cf931fc/Sphinx-1.6.1-py2.py3-none-any.whl",
    )
    version(
        "1.5.5",
        sha256="11f271e7a9398385ed730e90f0bb41dc3815294bdcd395b46ed2d033bc2e7d87",
        url="https://pypi.org/packages/5e/66/760dc216df24dc890dc87741631af02f81659105d970a30e5a80c6c8cf75/Sphinx-1.5.5-py2.py3-none-any.whl",
    )
    version(
        "1.4.5",
        sha256="a1901af3d437473662daca2ee8f03c232d84af08a0b119d6bc55020661b12ab8",
        url="https://pypi.org/packages/d1/ad/9fe56e099e0bd288f1fdc037c2146b0698e2cba1d9a48636660f39a0e791/Sphinx-1.4.5-py2.py3-none-any.whl",
    )
    version(
        "1.4",
        sha256="d4eda728fa077373f48468693376850016b11959fd23d5abef6b693ac6e0ef6b",
        url="https://pypi.org/packages/f1/01/6e6f29c3dbc57dddfd82710128f23c1be10a814c9fd4e77525fb3e6157d1/Sphinx-1.4-py2.py3-none-any.whl",
    )
    version(
        "1.3.1",
        sha256="2ddf18da3b0621fa43fee4b7290da0ae789b46fb899278a8acccda195c4979a7",
        url="https://pypi.org/packages/63/2c/0a30c391708f827039be5569164ed039b1e46906a4bff5a348b0abe2945e/Sphinx-1.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@7.2:")
        depends_on("python@3.8:", when="@6:7.1")
        depends_on("py-alabaster@0.7:", when="@1.7.5:")
        depends_on("py-babel@2.9:", when="@5.2:")
        depends_on("py-babel@1.3:", when="@3:5.1")
        depends_on("py-babel@1.3:1,2.1:", when="@1.7.5:2")
        depends_on("py-colorama@0.4.5:", when="@5.2: platform=windows")
        depends_on("py-colorama@0.3.5:", when="@1.7.5:5.1 platform=windows")
        depends_on("py-docutils@0.18.1:0.20", when="@7.0.1:")
        depends_on("py-docutils@0.18.1:0.19", when="@6.2:7.0.0")
        depends_on("py-docutils@0.18:0.19", when="@6:6.1")
        depends_on("py-docutils@0.14:0.19", when="@5.1:5")
        depends_on("py-docutils@0.14:0.18", when="@5:5.0")
        depends_on("py-docutils@0.14:0.17", when="@4.0.0-beta2:4")
        depends_on("py-docutils@0.12:0.16", when="@3.5.4:3")
        depends_on("py-docutils@0.12:", when="@2:2.4.4,3:3.5.3")
        depends_on("py-docutils@0.11:", when="@1.7.5:1.8.5")
        depends_on("py-imagesize@1.3:", when="@5.2:")
        depends_on("py-imagesize", when="@1.7.5:5.1")
        depends_on("py-importlib-metadata@4.8:", when="@5.2: ^python@:3.9")
        depends_on("py-importlib-metadata@4.4:", when="@4.4:5.1 ^python@:3.9")
        depends_on("py-jinja2@3.0.0:", when="@5.2:")
        depends_on("py-jinja2@2.3:2", when="@4.0.0:4.0.1")
        depends_on("py-jinja2@2.3:", when="@1.7.5:4.0.0-beta2,4.0.2:5.1")
        depends_on("py-markupsafe@:1", when="@4.0.0:4.0.1")
        depends_on("py-packaging@21:", when="@5.2:")
        depends_on("py-packaging", when="@1.7.5:5.1")
        depends_on("py-pygments@2.14:", when="@7.2:")
        depends_on("py-pygments@2.13:", when="@6.0.1:7.1")
        depends_on("py-pygments@2.12:", when="@5.2:6.0.0")
        depends_on("py-pygments@2.0:", when="@1.7.5:5.1")
        depends_on("py-requests@2.25:", when="@6.0.0:")
        depends_on("py-requests@2.5:", when="@2:6.0.0-beta2")
        depends_on("py-requests@2:", when="@1.7.5:1")
        depends_on("py-setuptools", when="@1.7.5:4.3")
        depends_on("py-six@1.5:", when="@1.7.5:1")
        depends_on("py-snowballstemmer@2:", when="@5.2:")
        depends_on("py-snowballstemmer@1.1:", when="@1.7.5:5.1")
        depends_on("py-sphinxcontrib-applehelp", when="@2:")
        depends_on("py-sphinxcontrib-devhelp", when="@2:")
        depends_on("py-sphinxcontrib-htmlhelp@2:", when="@4.1.1:")
        depends_on("py-sphinxcontrib-htmlhelp", when="@2:4.1.0")
        depends_on("py-sphinxcontrib-jsmath", when="@2:")
        depends_on("py-sphinxcontrib-qthelp", when="@2:")
        depends_on("py-sphinxcontrib-serializinghtml@1.1.9:", when="@7.2.3:")
        depends_on("py-sphinxcontrib-serializinghtml@1.1.5:", when="@4.1.1:7.2.2")
        depends_on("py-sphinxcontrib-serializinghtml", when="@2:4.1.0")
        depends_on("py-sphinxcontrib-websupport", when="@1.7.5:1")

    # Historical dependencies
