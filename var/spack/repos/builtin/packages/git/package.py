# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Git(AutotoolsPackage):
    """Git is a free and open source distributed version control
    system designed to handle everything from small to very large
    projects with speed and efficiency.
    """

    homepage = "http://git-scm.com"
    url = "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.12.0.tar.gz"
    maintainers("jennfshr")

    tags = ["build-tools"]

    executables = ["^git$"]

    # Every new git release comes with a corresponding manpage resource:
    # https://www.kernel.org/pub/software/scm/git/git-manpages-{version}.tar.gz
    # https://mirrors.edge.kernel.org/pub/software/scm/git/sha256sums.asc
    version("2.39.2", sha256="fb6807d1eb4094bb2349ab97d203fe1e6c3eb28af73ea391decfbd3a03c02e85")
    version("2.39.1", sha256="ae8d3427e4ccd677abc931f16183c0ec953e3bfcd866493601351e04a2b97398")
    version("2.38.3", sha256="ba8f1c56763cfde0433657b045629a4c55047c243eb3091d39dea6f281c8d8e1")
    version("2.37.5", sha256="5c11f90652afee6c77ef7ddfc672facd4bc6f2596d9627df2f1780664b058b9a")
    version("2.36.3", sha256="0c831b88b0534f08051d1287505dfe45c367108ee043de6f1c0502711a7aa3a6")
    version("2.35.6", sha256="6bd51e0487028543ba40fe3d5b33bd124526a7f7109824aa7f022e79edf93bd1")
    version("2.34.6", sha256="01c0ae4161a07ffeb89cfb8bda564eb2dcb83b45b678cf2930cdbdd8e81784d0")
    version("2.33.6", sha256="76f6a64a198bec38e83044f97fb5a2dfa8404091df5a905404615d2a4c5ebfb7")
    version("2.32.5", sha256="9982e17209cf4a385ce4a6167863cdd29f68e425d4249aac186434dc3536fe5f")
    version("2.31.6", sha256="73971208dccdd6d87639abe50ee3405421ec4ba05dec9f8aa90b4e7f1985e15c")
    version("2.30.7", sha256="c98bf38a296f23ad5619a097df928044b31859df8f89b3ae5a8ea109d3ebd88e")

    # Deprecated versions
    version(
        "2.38.1",
        sha256="620ed3df572a34e782a2be4c7d958d443469b2665eac4ae33f27da554d88b270",
        deprecated=True,
    )
    version(
        "2.37.0",
        sha256="fc3ffe6c65c1f7c681a1ce6bb91703866e432c762731d4b57c566d696f6d62c3",
        deprecated=True,
    )
    version(
        "2.37.4",
        sha256="a638c9bf9e45e8d48592076266adaa9b7aa272a99ee2aee2e166a649a9ba8a03",
        deprecated=True,
    )
    version(
        "2.36.4",
        sha256="8b99bd166d904103eccf90b7a9681247a1fb7eba82a72aba70625d9eb95c3db4",
        deprecated=True,
    )
    version(
        "2.36.1",
        sha256="37d936fd17c81aa9ddd3dba4e56e88a45fa534ad0ba946454e8ce818760c6a2c",
        deprecated=True,
    )
    version(
        "2.35.5",
        sha256="2cca63fe7bebb5b4bf8efea7b46b12bb89c16ff9711b6b6d845928501d00d0a3",
        deprecated=True,
    )
    version(
        "2.35.2",
        sha256="0decc02a47e792f522df3183c38a61ad8fbb38927502ca6781467a6599a888cb",
        deprecated=True,
    )
    version(
        "2.35.1",
        sha256="9845a37dd01f9faaa7d8aa2078399d3aea91b43819a5efea6e2877b0af09bd43",
        deprecated=True,
    )
    version(
        "2.35.0",
        sha256="c1d0adc777a457a3d9b2759024f173b34e61be96f7480ac5bc44216617834412",
        deprecated=True,
    )
    version(
        "2.34.5",
        sha256="26831c5e48a8c2bf6a4fede1b38e1e51ffd6dad85952cf69ac520ebd81a5ae82",
        deprecated=True,
    )
    version(
        "2.34.1",
        sha256="fc4eb5ecb9299db91cdd156c06cdeb41833f53adc5631ddf8c0cb13eaa2911c1",
        deprecated=True,
    )
    version(
        "2.34.0",
        sha256="0ce6222bfd31938b29360150286b51c77c643fa97740b1d35b6d1ceef8b0ecd7",
        deprecated=True,
    )
    version(
        "2.33.5",
        sha256="d061ed97f890befaef18b4aad80a37b40db90bcf24113c42765fee157a69c7de",
        deprecated=True,
    )
    version(
        "2.33.1",
        sha256="02047f8dc8934d57ff5e02aadd8a2fe8e0bcf94a7158da375e48086cc46fce1d",
        deprecated=True,
    )
    version(
        "2.33.0",
        sha256="02d909d0bba560d3a1008bd00dd577621ffb57401b09175fab2bf6da0e9704ae",
        deprecated=True,
    )
    version(
        "2.32.4",
        sha256="4c791b8e1d96948c9772efc21373ab9b3187af42cdebc3bcbb1a06d794d4e494",
        deprecated=True,
    )
    version(
        "2.32.0",
        sha256="6038f06d396ba9dab2eee541c7db6e7f9f847f181ec62f3d8441893f8c469398",
        deprecated=True,
    )
    version(
        "2.31.5",
        sha256="2d4197660322937cc44cab5742deef727ba519ef7405455e33100912e3b019f2",
        deprecated=True,
    )
    version(
        "2.31.1",
        sha256="46d37c229e9d786510e0c53b60065704ce92d5aedc16f2c5111e3ed35093bfa7",
        deprecated=True,
    )
    version(
        "2.31.0",
        sha256="bc6168777883562569144d536e8a855b12d25d46870d95188a3064260d7784ee",
        deprecated=True,
    )
    version(
        "2.30.6",
        sha256="a6130b38843a5c80e80fb4f7ac4864d361cbf103d262b64e267264e49440d24a",
        deprecated=True,
    )
    version(
        "2.30.1",
        sha256="23a3e53f0d2dd3e62a8147b24a1a91d6ffe95b92123ef4dbae04e9a6205e71c0",
        deprecated=True,
    )
    version(
        "2.30.0",
        sha256="d24c4fa2a658318c2e66e25ab67cc30038a35696d2d39e6b12ceccf024de1e5e",
        deprecated=True,
    )
    version(
        "2.29.2",
        sha256="869a121e1d75e4c28213df03d204156a17f02fce2dc77be9795b327830f54195",
        deprecated=True,
    )
    version(
        "2.29.0",
        sha256="fa08dc8424ef80c0f9bf307877f9e2e49f1a6049e873530d6747c2be770742ff",
        deprecated=True,
    )
    version(
        "2.28.0",
        sha256="f914c60a874d466c1e18467c864a910dd4ea22281ba6d4d58077cb0c3f115170",
        deprecated=True,
    )
    version(
        "2.27.0",
        sha256="77ded85cbe42b1ffdc2578b460a1ef5d23bcbc6683eabcafbb0d394dffe2e787",
        deprecated=True,
    )
    version(
        "2.26.0",
        sha256="aa168c2318e7187cd295a645f7370cc6d71a324aafc932f80f00c780b6a26bed",
        deprecated=True,
    )
    version(
        "2.25.0",
        sha256="a98c9b96d91544b130f13bf846ff080dda2867e77fe08700b793ab14ba5346f6",
        deprecated=True,
    )
    version(
        "2.23.0",
        sha256="e3396c90888111a01bf607346db09b0fbf49a95bc83faf9506b61195936f0cfe",
        deprecated=True,
    )
    version(
        "2.22.0",
        sha256="a4b7e4365bee43caa12a38d646d2c93743d755d1cea5eab448ffb40906c9da0b",
        deprecated=True,
    )
    version(
        "2.21.0",
        sha256="85eca51c7404da75e353eba587f87fea9481ba41e162206a6f70ad8118147bee",
        deprecated=True,
    )
    version(
        "2.20.1",
        sha256="edc3bc1495b69179ba4e272e97eff93334a20decb1d8db6ec3c19c16417738fd",
        deprecated=True,
    )
    version(
        "2.19.2",
        sha256="db893ad69c9ac9498b09677c5839787eba2eb3b7ef2bc30bfba7e62e77cf7850",
        deprecated=True,
    )
    version(
        "2.19.1",
        sha256="ec4dc96456612c65bf6d944cee9ac640145ec7245376832b781cb03e97cbb796",
        deprecated=True,
    )
    version(
        "2.18.0",
        sha256="94faf2c0b02a7920b0b46f4961d8e9cad08e81418614102898a55f980fa3e7e4",
        deprecated=True,
    )
    version(
        "2.17.1",
        sha256="ec6452f0c8d5c1f3bcceabd7070b8a8a5eea11d4e2a04955c139b5065fd7d09a",
        deprecated=True,
    )
    version(
        "2.17.0",
        sha256="7a0cff35dbb14b77dca6924c33ac9fe510b9de35d5267172490af548ec5ee1b8",
        deprecated=True,
    )
    version(
        "2.15.1",
        sha256="85fca8781a83c96ba6db384cc1aa6a5ee1e344746bafac1cbe1f0fe6d1109c84",
        deprecated=True,
    )
    version(
        "2.14.1",
        sha256="01925349b9683940e53a621ee48dd9d9ac3f9e59c079806b58321c2cf85a4464",
        deprecated=True,
    )
    version(
        "2.13.0",
        sha256="9f2fa8040ebafc0c2caae4a9e2cb385c6f16c0525bcb0fbd84938bc796372e80",
        deprecated=True,
    )
    version(
        "2.12.2",
        sha256="d9c6d787a24670d7e5100db2367c250ad9756ef8084fb153a46b82f1d186f8d8",
        deprecated=True,
    )
    version(
        "2.12.1",
        sha256="65d62d10caf317fc1daf2ca9975bdb09dbff874c92d24f9529d29a7784486b43",
        deprecated=True,
    )
    version(
        "2.12.0",
        sha256="882f298daf582a07c597737eb4bbafb82c6208fe0e73c047defc12169c221a92",
        deprecated=True,
    )
    version(
        "2.11.1",
        sha256="a1cdd7c820f92c44abb5003b36dc8cb7201ba38e8744802399f59c97285ca043",
        deprecated=True,
    )
    version(
        "2.11.0",
        sha256="d3be9961c799562565f158ce5b836e2b90f38502d3992a115dfb653d7825fd7e",
        deprecated=True,
    )
    version(
        "2.9.3",
        sha256="a252b6636b12d5ba57732c8469701544c26c2b1689933bd1b425e603cbb247c0",
        deprecated=True,
    )
    version(
        "2.9.2",
        sha256="3cb09a3917c2d8150fc1708f3019cf99a8f0feee6cd61bba3797e3b2a85be9dc",
        deprecated=True,
    )
    version(
        "2.9.1",
        sha256="c2230873bf77f93736473e6a06501bf93eed807d011107de6983dc015424b097",
        deprecated=True,
    )
    version(
        "2.9.0",
        sha256="bff7560f5602fcd8e37669e0f65ef08c6edc996e4f324e4ed6bb8a84765e30bd",
        deprecated=True,
    )
    version(
        "2.8.4",
        sha256="626e319f8a24fc0866167ea5f6bf3e2f38f69d6cb2e59e150f13709ca3ebf301",
        deprecated=True,
    )
    version(
        "2.8.3",
        sha256="2dad50c758339d6f5235309db620e51249e0000ff34aa2f2acbcb84c2123ed09",
        deprecated=True,
    )
    version(
        "2.8.2",
        sha256="a029c37ee2e0bb1efea5c4af827ff5afdb3356ec42fc19c1d40216d99e97e148",
        deprecated=True,
    )
    version(
        "2.8.1",
        sha256="cfc66324179b9ed62ee02833f29d39935f4ab66874125a3ab9d5bb9055c0cb67",
        deprecated=True,
    )
    version(
        "2.8.0",
        sha256="2c6eee5506237e0886df9973fd7938a1b2611ec93d07f64ed3447493ebac90d1",
        deprecated=True,
    )
    version(
        "2.7.3",
        sha256="30d067499b61caddedaf1a407b4947244f14d10842d100f7c7c6ea1c288280cd",
        deprecated=True,
    )
    version(
        "2.7.1",
        sha256="b4ab42798b7fb038eaefabb0c32ce9dbde2919103e5e2a35adc35dd46258a66f",
        deprecated=True,
    )

    for _version, _sha256_manpage in {
        "2.39.2": "fd92e67fb750ceb2279dcee967a21303f2f8117834a21c1e0c9f312ebab6d254",
        "2.39.1": "b2d1b2c6cba2343934792c4409a370a8c684add1b3c0f9b757e71189b1a2e80e",
        "2.38.3": "9e5c924f6f1c961e09d1a8926c2775a158a0375a3311205d7a6176a3ed522272",
        "2.38.1": "fcb27484406b64419a9f9890e95ef29af08e1f911d9d368546eddc59a18e245d",
        "2.37.5": "9fab559197891fc1b499cb57513effce7462383f861ac6a7791a46f5348dd7fe",
        "2.37.4": "06ed920949e717f3ab13c98327ee63cae5e3020ac657d14513ef8f843109b638",
        "2.37.0": "69386ab0dcdbc8398ebb97487733166033f1c7711b02b8861b1ae8f4f46e6e4e",
        "2.36.3": "c5f5385c2b46270a8ce062a9c510bfa4288d9cca54efe0dff48a12ca969cfc6f",
        "2.36.6": "c5f5385c2b46270a8ce062a9c510bfa4288d9cca54efe0dff48a12ca969cfc6f",
        "2.36.1": "3fcd315976f06b54b0abb9c14d38c3d484f431ea4de70a706cc5dddc1799f4f7",
        "2.35.6": "5e44e05a97f49d7a170a7303f795063b19bc78560acd7458274882f19b631187",
        "2.35.5": "6cbd4d2185c7a757db21f873973fa1efb81069d8b8b8cc350ca6735cb98f45c5",
        "2.35.2": "86e153bdd96edd8462cb7a5c57be1b2b670b033c18272b0aa2e6a102acce50be",
        "2.35.1": "d90da8b28fe0088519e0dc3c9f4bc85e429c7d6ccbaadcfe94aed47fb9c95504",
        "2.35.0": "c0408a1c944c8e481d7f507bd90a7ee43c34617a1a7af2d76a1898dcf44fa430",
        "2.34.6": "70c784ced9c5ccbd4137d676b032e2ccffeea8aef3094626c2b44d6c843547df",
        "2.34.5": "897941be5b223b9d32217adb64ea8747db2ba57be5f68be598c44d747d1061b2",
        "2.34.1": "220f1ed68582caeddf79c4db15e4eaa4808ec01fd11889e19232f0a74d7f31b0",
        "2.34.0": "fe66a69244def488306c3e05c1362ea53d8626d2a7e57cd7311df2dab1ef8356",
        "2.33.6": "d7b9170dc7d6f461e00731cf5cf6e4b589e90c8d4eac440fd3e8b5e3d11f0b8f",
        "2.33.5": "34648ede9ac2869190083ee826065c36165e54d9e2906b10680261b243d89890",
        "2.33.1": "292b08ca1b79422ff478a6221980099c5e3c0a38aba39d952063eedb68e27d93",
        "2.33.0": "ba9cd0f29a3632a3b78f8ed2389f0780aa6e8fcbe258259d7c584920d19ed1f7",
        "2.32.5": "99b236824f1677e15b21514e310d7a0954586d031ffc3a873a4e2138ed073f15",
        "2.32.4": "fa73d0eac384e594efdd4c21343545e407267ab64e970a6b395c7f1874ddb0bf",
        "2.32.0": "b5533c40ea1688231c0e2df51cc0d1c0272e17fe78a45ba6e60cb8f61fa4a53c",
        "2.31.6": "2e2f921d8ef8a839e05ba3a1cea8f864a49b04648378bf0253213a5d4f1642fe",
        "2.31.5": "18850fc8f1c34e51a0a98b9f974b8356a5d63a53c96fb9fe3dc2880ee84746ab",
        "2.31.1": "d330498aaaea6928b0abbbbb896f6f605efd8d35f23cbbb2de38c87a737d4543",
        "2.31.0": "a51b760c36be19113756839a9110b328a09abfff0d57f1c93ddac3974ccbc238",
        "2.30.7": "4fc6063c229453de244a88c71f688a2508f30b80ebd47353cc68d730ea1b82aa",
        "2.30.6": "6c20ab10be233e8ff7838351fa5210e972c08005ec541a5241f626cfd4adebfe",
        "2.30.1": "db323e1b242e9d0337363b1e538c8b879e4c46eedbf94d3bee9e65dab6d49138",
        "2.30.0": "e23035ae232c9a5eda57db258bc3b7f1c1060cfd66920f92c7d388b6439773a6",
        "2.29.2": "68b258e6d590cb78e02c0df741bbaeab94cbbac6d25de9da4fb3882ee098307b",
        "2.29.0": "8f3bf70ddb515674ce2e19572920a39b1be96af12032b77f1dd57898981fb151",
        "2.28.0": "3cfca28a88d5b8112ea42322b797a500a14d0acddea391aed0462aff1ab11bf7",
        "2.27.0": "414e4b17133e54d846f6bfa2479f9757c50e16c013eb76167a492ae5409b8947",
        "2.26.0": "c1ffaf0b4cd1e80a0eb0d4039e208c9d411ef94d5da44e38363804e1a7961218",
        "2.25.0": "22b2380842ef75e9006c0358de250ead449e1376d7e5138070b9a3073ef61d44",
        "2.23.0": "a5b0998f95c2290386d191d34780d145ea67e527fac98541e0350749bf76be75",
        "2.22.0": "f6a5750dfc4a0aa5ec0c0cc495d4995d1f36ed47591c3941be9756c1c3a1aa0a",
        "2.21.0": "14c76ebb4e31f9e55cf5338a04fd3a13bced0323cd51794ccf45fc74bd0c1080",
        "2.20.1": "e9c123463abd05e142defe44a8060ce6e9853dfd8c83b2542e38b7deac4e6d4c",
        "2.19.2": "60334ecd59ee10319af4a7815174d10991d1afabacd3b3129d589f038bf25542",
        "2.19.1": "bd27f58dc90a661e3080b97365eb7322bfa185de95634fc59d98311925a7d894",
        "2.18.0": "6cf38ab3ad43ccdcd6a73ffdcf2a016d56ab6b4b240a574b0bb96f520a04ff55",
        "2.17.1": "9732053c1a618d2576c1751d0249e43702f632a571f84511331882beb360677d",
        "2.17.0": "41b58c68e90e4c95265c75955ddd5b68f6491f4d57b2f17c6d68e60bbb07ba6a",
        "2.15.1": "472454c494c9a7f50ad38060c3eec372f617de654b20f3eb3be59fc17a683fa1",
        "2.14.1": "8c5810ce65d44cd333327d3a115c5b462712a2f81225d142e07bd889ad8dc0e0",
        "2.13.0": "e764721796cad175a4cf9a4afe7fb4c4fc57582f6f9a6e214239498e0835355b",
        "2.12.2": "6e7ed503f1190734e57c9427df356b42020f125fa36ab0478777960a682adf50",
        "2.12.1": "35e46b8acd529ea671d94035232b1795919be8f3c3a363ea9698f1fd08d7d061",
        "2.12.0": "1f7733a44c59f9ae8dd321d68a033499a76c82046025cc2a6792299178138d65",
        "2.11.1": "ee567e7b0f95333816793714bb31c54e288cf8041f77a0092b85e62c9c2974f9",
        "2.11.0": "437a0128acd707edce24e1a310ab2f09f9a09ee42de58a8e7641362012dcfe22",
        "2.9.3": "8ea1a55b048fafbf0c0c6fcbca4b5b0f5e9917893221fc7345c09051d65832ce",
        "2.9.2": "ac5c600153d1e4a1c6494e250cd27ca288e7667ad8d4ea2f2386f60ba1b78eec",
        "2.9.1": "324f5f173f2bd50b0102b66e474b81146ccc078d621efeb86d7f75e3c1de33e6",
        "2.9.0": "35ba69a8560529aa837e395a6d6c8d42f4d29b40a3c1cc6e3dc69bb1faadb332",
        "2.8.4": "953a8eadaf4ae96dbad2c3ec12384c677416843917ef83d94b98367ffd55afc0",
        "2.8.3": "2dad50c758339d6f5235309db620e51249e0000ff34aa2f2acbcb84c2123ed09",
        "2.8.2": "82d322211aade626d1eb3bcf3b76730bfdd2fcc9c189950fb0a8bdd69c383e2f",
        "2.8.1": "df46de0c172049f935cc3736361b263c5ff289b77077c73053e63ae83fcf43f4",
        "2.8.0": "2c48902a69df3bec3b8b8f0350a65fd1b662d2f436f0e64d475ecd1c780767b6",
        "2.7.3": "84b487c9071857ab0f15f11c4a102a583d59b524831cda0dc0954bd3ab73920b",
        "2.7.1": "0313cf4d283336088883d8416692fb6c547512233e11dbf06e5b925b7e762d61",
    }.items():
        resource(
            name="git-manpages",
            url="https://www.kernel.org/pub/software/scm/git/git-manpages-{0}.tar.gz".format(
                _version
            ),
            sha256=_sha256_manpage,
            placement="git-manpages",
            when="@{0} +man".format(_version),
        )

    variant("tcltk", default=False, description="Gitk: provide Tcl/Tk in the run environment")
    variant("svn", default=False, description="Provide SVN Perl dependency in run environment")
    variant("perl", default=True, description="Do not use Perl scripts or libraries at all")
    variant("nls", default=True, description="Enable native language support")
    variant("man", default=True, description="Install manual pages")
    variant("subtree", default=True, description="Add git-subtree command and capability")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("curl")
    depends_on("expat")
    depends_on("gettext", when="+nls")
    depends_on("iconv")
    depends_on("libidn2")
    depends_on("openssl")
    depends_on("pcre", when="@:2.13")
    depends_on("pcre2", when="@2.14:")
    depends_on("perl", when="+perl")
    depends_on("zlib")
    depends_on("openssh", type="run")
    depends_on("perl-alien-svn", type="run", when="+svn")
    depends_on("tk", type=("build", "link"), when="+tcltk")

    conflicts("+svn", when="~perl")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(spack.fetch_strategy.GitFetchStrategy.git_version_re, output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        prefix = os.path.dirname(exes[0])
        variants = ""
        if "gitk" in os.listdir(prefix):
            variants += "+tcltk"
        else:
            variants += "~tcltk"
        return variants

    # See the comment in setup_build_environment re EXTLIBS.
    def patch(self):
        filter_file(r"^EXTLIBS =$", "#EXTLIBS =", "Makefile")

    def setup_build_environment(self, env):
        # We use EXTLIBS rather than LDFLAGS so that git's Makefile
        # inserts the information into the proper place in the link commands
        # (alongside the # other libraries/paths that configure discovers).
        # LDFLAGS is inserted *before* libgit.a, which requires libintl.
        # EXTFLAGS is inserted *after* libgit.a.
        # This depends on the patch method above, which keeps the Makefile
        # from stepping on the value that we pass in via the environment.
        #
        # The test avoids failures when git is an external package.
        # In that case the node in the DAG gets truncated and git DOES NOT
        # have a gettext dependency.
        if "+nls" in self.spec:
            if "intl" in self.spec["gettext"].libs.names:
                env.append_flags("EXTLIBS", "-L{0} -lintl".format(self.spec["gettext"].prefix.lib))
            env.append_flags("CFLAGS", "-I{0}".format(self.spec["gettext"].prefix.include))

        if "~perl" in self.spec:
            env.append_flags("NO_PERL", "1")

    def configure_args(self):
        spec = self.spec

        configure_args = [
            "--with-curl={0}".format(spec["curl"].prefix),
            "--with-expat={0}".format(spec["expat"].prefix),
            "--with-iconv={0}".format(spec["iconv"].prefix),
            "--with-openssl={0}".format(spec["openssl"].prefix),
            "--with-zlib={0}".format(spec["zlib"].prefix),
        ]

        if "+perl" in self.spec:
            configure_args.append("--with-perl={0}".format(spec["perl"].command.path))

        if "^pcre" in self.spec:
            configure_args.append("--with-libpcre={0}".format(spec["pcre"].prefix))
        if "^pcre2" in self.spec:
            configure_args.append("--with-libpcre2={0}".format(spec["pcre2"].prefix))
        if "+tcltk" in self.spec:
            configure_args.append("--with-tcltk={0}".format(self.spec["tk"].prefix.bin.wish))
        else:
            configure_args.append("--without-tcltk")

        return configure_args

    @run_after("configure")
    def filter_rt(self):
        if self.spec.satisfies("platform=darwin"):
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r" -lrt$", "", "Makefile")

    def check(self):
        make("test")

    def build(self, spec, prefix):
        args = []
        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            with working_dir("contrib/credential/osxkeychain"):
                make()

    def install(self, spec, prefix):
        args = ["install"]
        if "~nls" in self.spec:
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            install(
                "contrib/credential/osxkeychain/git-credential-osxkeychain",
                join_path(prefix, "libexec", "git-core"),
            )

    @run_after("install")
    def install_completions(self):
        install_tree("contrib/completion", self.prefix.share)

    @run_after("install")
    def install_manpages(self):
        if "~man" in self.spec:
            return

        prefix = self.prefix

        with working_dir("git-manpages"):
            install_tree("man1", prefix.share.man.man1)
            install_tree("man5", prefix.share.man.man5)
            install_tree("man7", prefix.share.man.man7)

    @run_after("install")
    def install_subtree(self):
        if "+subtree" in self.spec:
            with working_dir("contrib/subtree"):
                make_args = ["V=1", "prefix={}".format(self.prefix.bin)]
                make(" ".join(make_args))
                install_args = ["V=1", "prefix={}".format(self.prefix.bin), "install"]
                make(" ".join(install_args))
                install("git-subtree", self.prefix.bin)

    def setup_run_environment(self, env):
        # Setup run environment if using SVN extension
        # Libs from perl-alien-svn and apr-util are required in
        # LD_LIBRARY_PATH
        # TODO: extend to other platforms
        if "+svn platform=linux" in self.spec:
            perl_svn = self.spec["perl-alien-svn"]
            env.prepend_path(
                "LD_LIBRARY_PATH",
                join_path(
                    perl_svn.prefix, "lib", "perl5", "x86_64-linux-thread-multi", "Alien", "SVN"
                ),
            )
