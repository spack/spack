# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import spack.build_environment
from spack.package import *


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """

    homepage = "https://www.cmake.org"
    url = "https://github.com/Kitware/CMake/releases/download/v3.19.0/cmake-3.19.0.tar.gz"
    git = "https://gitlab.kitware.com/cmake/cmake.git"

    maintainers("alalazo", "johnwparent")

    tags = ["build-tools", "windows"]

    executables = ["^cmake[0-9]*$"]

    version("master", branch="master")
    version("3.27.8", sha256="fece24563f697870fbb982ea8bf17482c9d5f855d8c9bf0b82463d76c9e8d0cc")
    version("3.27.7", sha256="08f71a106036bf051f692760ef9558c0577c42ac39e96ba097e7662bd4158d8e")
    version("3.27.6", sha256="ef3056df528569e0e8956f6cf38806879347ac6de6a4ff7e4105dc4578732cfb")
    version("3.27.4", sha256="0a905ca8635ca81aa152e123bdde7e54cbe764fdd9a70d62af44cad8b92967af")
    version("3.27.3", sha256="66afdc0f181461b70b6fedcde9ecc4226c5cd184e7203617c83b7d8e47f49521")
    version("3.27.2", sha256="798e50085d423816fe96c9ef8bee5e50002c9eca09fed13e300de8a91d35c211")
    version("3.27.1", sha256="b1a6b0135fa11b94476e90f5b32c4c8fad480bf91cf22d0ded98ce22c5132004")
    version("3.27.0", sha256="aaeddb6b28b993d0a6e32c88123d728a17561336ab90e0bf45032383564d3cb8")
    version("3.26.5", sha256="c0970b1e44a7fbca4322997ce05dac521b04748fe424922152faf22d20782bf9")
    version("3.26.4", sha256="313b6880c291bd4fe31c0aa51d6e62659282a521e695f30d5cc0d25abbd5c208")
    version("3.26.3", sha256="bbd8d39217509d163cb544a40d6428ac666ddc83e22905d3e52c925781f0f659")
    version("3.26.2", sha256="d54f25707300064308ef01d4d21b0f98f508f52dda5d527d882b9d88379f89a8")
    version("3.26.1", sha256="f29964290ad3ced782a1e58ca9fda394a82406a647e24d6afd4e6c32e42c412f")
    version("3.26.0", sha256="4256613188857e95700621f7cdaaeb954f3546a9249e942bc2f9b3c26e381365")
    version("3.25.3", sha256="cc995701d590ca6debc4245e9989939099ca52827dd46b5d3592f093afe1901c")
    version("3.25.2", sha256="c026f22cb931dd532f648f087d587f07a1843c6e66a3dfca4fb0ea21944ed33c")
    version("3.25.1", sha256="1c511d09516af493694ed9baf13c55947a36389674d657a2d5e0ccedc6b291d8")
    version("3.25.0", sha256="306463f541555da0942e6f5a0736560f70c487178b9d94a5ae7f34d0538cdd48")
    version("3.24.4", sha256="32c9e499510eff7070d3f0adfbabe0afea2058608c5fa93e231beb49fbfa2296")
    version("3.24.3", sha256="b53aa10fa82bff84ccdb59065927b72d3bee49f4d86261249fc0984b3b367291")
    version("3.24.2", sha256="0d9020f06f3ddf17fb537dc228e1a56c927ee506b486f55fe2dc19f69bf0c8db")
    version("3.24.1", sha256="4931e277a4db1a805f13baa7013a7757a0cbfe5b7932882925c7061d9d1fa82b")
    version("3.24.0", sha256="c2b61f7cdecb1576cad25f918a8f42b8685d88a832fd4b62b9e0fa32e915a658")
    version("3.23.5", sha256="f2944cde7a140b992ba5ccea2009a987a92413762250de22ebbace2319a0f47d")
    version("3.23.4", sha256="aa8b6c17a5adf04de06e42c06adc7e25b21e4fe8378f44f703a861e5f6ac59c7")
    version("3.23.3", sha256="06fefaf0ad94989724b56f733093c2623f6f84356e5beb955957f9ce3ee28809")
    version("3.23.2", sha256="f316b40053466f9a416adf981efda41b160ca859e97f6a484b447ea299ff26aa")
    version("3.23.1", sha256="33fd10a8ec687a4d0d5b42473f10459bb92b3ae7def2b745dc10b192760869f3")
    version("3.23.0", sha256="5ab0a12f702f44013be7e19534cd9094d65cc9fe7b2cd0f8c9e5318e0fe4ac82")
    version("3.22.6", sha256="73933163670ea4ea95c231549007b0c7243282293506a2cf4443714826ad5ec3")
    version("3.22.5", sha256="d3987c3f7759fa0a401c5fcd5076be44a19613bfaa8baee1b5d1835750dc5375")
    version("3.22.4", sha256="5c55d0b0bc4c191549e3502b8f99a4fe892077611df22b4178cc020626e22a47")
    version("3.22.3", sha256="9f8469166f94553b6978a16ee29227ec49a2eb5ceb608275dec40d8ae0d1b5a0")
    version("3.22.2", sha256="3c1c478b9650b107d452c5bd545c72e2fad4e37c09b89a1984b9a2f46df6aced")
    version("3.22.1", sha256="0e998229549d7b3f368703d20e248e7ee1f853910d42704aa87918c213ea82c0")
    version("3.22.0", sha256="998c7ba34778d2dfdb3df8a695469e24b11e2bfa21fbe41b361a3f45e1c9345e")
    version("3.21.7", sha256="3523c4a5afc61ac3d7c92835301cdf092129c9b672a6ee17e68c92e928c1375a")
    version("3.21.6", sha256="b7c3ac35ca7ed3cce8c192c9c873e6061aaecc8b2bc564290e629b10bff59f3c")
    version("3.21.5", sha256="c73587b5ab827d56c09f0a1e256b12743ff200495e31fc9686f2b9dc8a28897f")
    version("3.21.4", sha256="d9570a95c215f4c9886dd0f0564ca4ef8d18c30750f157238ea12669c2985978")
    version("3.21.3", sha256="d14d06df4265134ee42c4d50f5a60cb8b471b7b6a47da8e5d914d49dd783794f")
    version("3.21.2", sha256="94275e0b61c84bb42710f5320a23c6dcb2c6ee032ae7d2a616f53f68b3d21659")
    version("3.21.1", sha256="fac3915171d4dff25913975d712f76e69aef44bf738ba7b976793a458b4cfed4")
    version("3.21.0", sha256="4a42d56449a51f4d3809ab4d3b61fd4a96a469e56266e896ce1009b5768bd2ab")
    version("3.20.6", sha256="a0bd485e1a38dd13c0baec89d5f4adbf61c7fd32fddb38eabc69a75bc0b65d72")
    version("3.20.5", sha256="12c8040ef5c6f1bc5b8868cede16bb7926c18980f59779e299ab52cbc6f15bb0")
    version("3.20.4", sha256="87a4060298f2c6bb09d479de1400bc78195a5b55a65622a7dceeb3d1090a1b16")
    version("3.20.3", sha256="4d008ac3461e271fcfac26a05936f77fc7ab64402156fb371d41284851a651b8")
    version("3.20.2", sha256="aecf6ecb975179eb3bb6a4a50cae192d41e92b9372b02300f9e8f1d5f559544e")
    version("3.20.1", sha256="3f1808b9b00281df06c91dd7a021d7f52f724101000da7985a401678dfe035b0")
    version("3.20.0", sha256="9c06b2ddf7c337e31d8201f6ebcd3bba86a9a033976a9aee207fe0c6971f4755")
    version("3.19.8", sha256="09b4fa4837aae55c75fb170f6a6e2b44818deba48335d1969deddfbb34e30369")
    version("3.19.7", sha256="58a15f0d56a0afccc3cc5371234fce73fcc6c8f9dbd775d898e510b83175588e")
    version("3.19.6", sha256="ec87ab67c45f47c4285f204280c5cde48e1c920cfcfed1555b27fb3b1a1d20ba")
    version("3.19.5", sha256="c432296eb5dec6d71eae15d140f6297d63df44e9ffe3e453628d1dc8fc4201ce")
    version("3.19.4", sha256="7d0232b9f1c57e8de81f38071ef8203e6820fe7eec8ae46a1df125d88dbcc2e1")
    version("3.19.3", sha256="3faca7c131494a1e34d66e9f8972ff5369e48d419ea8ceaa3dc15b4c11367732")
    version("3.19.2", sha256="e3e0fd3b23b7fb13e1a856581078e0776ffa2df4e9d3164039c36d3315e0c7f0")
    version("3.19.1", sha256="1d266ea3a76ef650cdcf16c782a317cb4a7aa461617ee941e389cb48738a3aba")
    version("3.19.0", sha256="fdda688155aa7e72b7c63ef6f559fca4b6c07382ea6dca0beb5f45aececaf493")
    version("3.18.6", sha256="124f571ab70332da97a173cb794dfa09a5b20ccbb80a08e56570a500f47b6600")
    version("3.18.5", sha256="080bf24b0f73f4bf3ec368d2be1aa59369b9bb1cd693deeb6f18fe553ca74ab4")
    version("3.18.4", sha256="597c61358e6a92ecbfad42a9b5321ddd801fc7e7eca08441307c9138382d4f77")
    version("3.18.3", sha256="2c89f4e30af4914fd6fb5d00f863629812ada848eee4e2d29ec7e456d7fa32e5")
    version("3.18.2", sha256="5d4e40fc775d3d828c72e5c45906b4d9b59003c9433ff1b36a1cb552bbd51d7e")
    version("3.18.1", sha256="c0e3338bd37e67155b9d1e9526fec326b5c541f74857771b7ffed0c46ad62508")
    version("3.18.0", sha256="83b4ffcb9482a73961521d2bafe4a16df0168f03f56e6624c419c461e5317e29")
    version("3.17.5", sha256="8c3083d98fd93c1228d5e4e40dbff2dd88f4f7b73b9fa24a2938627b8bc28f1a")
    version("3.17.4", sha256="86985d73d0a63ec99c236aab5287316e252164f33d7c4cb160954a980c71f36f")
    version("3.17.3", sha256="0bd60d512275dc9f6ef2a2865426a184642ceb3761794e6b65bff233b91d8c40")
    version("3.17.1", sha256="3aa9114485da39cbd9665a0bfe986894a282d5f0882b1dea960a739496620727")
    version("3.17.0", sha256="b74c05b55115eacc4fa2b77a814981dbda05cdc95a53e279fe16b7b272f00847")
    version("3.16.9", sha256="1708361827a5a0de37d55f5c9698004c035abb1de6120a376d5d59a81630191f")
    version("3.16.8", sha256="177434021132686cb901fea7db9fa2345efe48d566b998961594d5cc346ac588")
    version("3.16.7", sha256="5f49c95a2933b1800f14840f3a389f4cef0b19093985a35053b43f38ec21358f")
    version("3.16.6", sha256="6f6ff1a197851b0fa8412ff5de602e6717a4eb9509b2c385b08589c4e7a16b62")
    version("3.16.5", sha256="5f760b50b8ecc9c0c37135fae5fbf00a2fef617059aa9d61c1bb91653e5a8bfc")
    version("3.16.4", sha256="9bcc8c114d9da603af9512083ed7d4a39911d16105466beba165ba8fe939ac2c")
    version("3.16.3", sha256="e54f16df9b53dac30fd626415833a6e75b0e47915393843da1825b096ee60668")
    version("3.16.2", sha256="8c09786ec60ca2be354c29829072c38113de9184f29928eb9da8446a5f2ce6a9")
    version("3.16.1", sha256="a275b3168fa8626eca4465da7bb159ff07c8c6cb0fb7179be59e12cbdfa725fd")
    version("3.16.0", sha256="6da56556c63cab6e9a3e1656e8763ed4a841ac9859fefb63cbe79472e67e8c5f")
    version("3.15.7", sha256="71999d8a14c9b51708847371250a61533439a7331eb7702ac105cfb3cb1be54b")
    version("3.15.6", sha256="3fa17992ac97d3fc856ffba5d3b10578744ea5b4736818f01e6067f0253b2db5")
    version("3.15.5", sha256="fbdd7cef15c0ced06bb13024bfda0ecc0dedbcaaaa6b8a5d368c75255243beb4")
    version("3.15.4", sha256="8a211589ea21374e49b25fc1fc170e2d5c7462b795f1b29c84dd0e984301ed7a")
    version("3.15.3", sha256="13958243a01365b05652fa01b21d40fa834f70a9e30efa69c02604e64f58b8f5")
    version("3.15.2", sha256="539088cb29a68e6d6a8fba5c00951e5e5b1a92c68fa38a83e1ed2f355933f768")
    version("3.15.1", sha256="18dec548d8f8b04d53c60f9cedcebaa6762f8425339d1e2c889c383d3ccdd7f7")
    version("3.15.0", sha256="0678d74a45832cacaea053d85a5685f3ed8352475e6ddf9fcb742ffca00199b5")
    version("3.14.7", sha256="9221993e0af3e6d10124d840ff24f5b2f3b884416fca04d3312cb0388dec1385")
    version("3.14.6", sha256="4e8ea11cabe459308671b476469eace1622e770317a15951d7b55a82ccaaccb9")
    version("3.14.5", sha256="505ae49ebe3c63c595fa5f814975d8b72848447ee13b6613b0f8b96ebda18c06")
    version("3.14.4", sha256="00b4dc9b0066079d10f16eed32ec592963a44e7967371d2f5077fd1670ff36d9")
    version("3.14.3", sha256="215d0b64e81307182b29b63e562edf30b3875b834efdad09b3fcb5a7d2f4b632")
    version("3.14.2", sha256="a3cbf562b99270c0ff192f692139e98c605f292bfdbc04d70da0309a5358e71e")
    version("3.14.1", sha256="7321be640406338fc12590609c42b0fae7ea12980855c1be363d25dcd76bb25f")
    version("3.14.0", sha256="aa76ba67b3c2af1946701f847073f4652af5cbd9f141f221c97af99127e75502")
    version("3.13.5", sha256="526db6a4b47772d1943b2f86de693e712f9dacf3d7c13b19197c9bef133766a5")
    version("3.13.4", sha256="fdd928fee35f472920071d1c7f1a6a2b72c9b25e04f7a37b409349aef3f20e9b")
    version("3.13.3", sha256="665f905036b1f731a2a16f83fb298b1fb9d0f98c382625d023097151ad016b25")
    version("3.13.2", sha256="c925e7d2c5ba511a69f43543ed7b4182a7d446c274c7480d0e42cd933076ae25")
    version("3.13.1", sha256="befe1ce6d672f2881350e94d4e3cc809697dd2c09e5b708b76c1dae74e1b2210")
    version("3.13.0", sha256="4058b2f1a53c026564e8936698d56c3b352d90df067b195cb749a97a3d273c90")
    version("3.12.4", sha256="5255584bfd043eb717562cff8942d472f1c0e4679c4941d84baadaa9b28e3194")
    version("3.12.3", sha256="acbf13af31a741794106b76e5d22448b004a66485fc99f6d7df4d22e99da164a")
    version("3.12.2", sha256="0f97485799e51a7070cc11494f3e02349b0fc3a24cc12b082e737bf67a0581a4")
    version("3.12.1", sha256="c53d5c2ce81d7a957ee83e3e635c8cda5dfe20c9d501a4828ee28e1615e57ab2")
    version("3.12.0", sha256="d0781a90f6cdb9049d104ac16a150f9350b693498b9dea8a0331e799db6b9d69")
    version("3.11.4", sha256="8f864e9f78917de3e1483e256270daabc4a321741592c5b36af028e72bff87f5")
    version("3.11.3", sha256="287135b6beb7ffc1ccd02707271080bbf14c21d80c067ae2c0040e5f3508c39a")
    version("3.11.2", sha256="5ebc22bbcf2b4c7a20c4190d42c084cf38680a85b1a7980a2f1d5b4a52bf5248")
    version("3.11.1", sha256="57bebc6ca4d1d42c6385249d148d9216087e0fda57a47dc5c858790a70217d0c")
    version("3.11.0", sha256="c313bee371d4d255be2b4e96fd59b11d58bc550a7c78c021444ae565709a656b")
    version("3.10.3", sha256="0c3a1dcf0be03e40cf4f341dda79c96ffb6c35ae35f2f911845b72dab3559cf8")
    version("3.10.2", sha256="80d0faad4ab56de07aa21a7fc692c88c4ce6156d42b0579c6962004a70a3218b")
    version("3.10.1", sha256="7be36ee24b0f5928251b644d29f5ff268330a916944ef4a75e23ba01e7573284")
    version("3.10.0", sha256="b3345c17609ea0f039960ef470aa099de9942135990930a57c14575aae884987")
    version("3.9.6", sha256="7410851a783a41b521214ad987bb534a7e4a65e059651a2514e6ebfc8f46b218")
    version("3.9.4", sha256="b5d86f12ae0072db520fdbdad67405f799eb728b610ed66043c20a92b4906ca1")
    version("3.9.2", sha256="954a5801a456ee48e76f01107c9a4961677dd0f3e115275bbd18410dc22ba3c1")
    version("3.9.0", sha256="167701525183dbb722b9ffe69fb525aa2b81798cf12f5ce1c020c93394dfae0f")
    version("3.8.2", sha256="da3072794eb4c09f2d782fcee043847b99bb4cf8d4573978d9b2024214d6e92d")
    version("3.8.1", sha256="ce5d9161396e06501b00e52933783150a87c33080d4bdcef461b5b7fd24ac228")
    version("3.8.0", sha256="cab99162e648257343a20f61bcd0b287f5e88e36fcb2f1d77959da60b7f35969")
    version("3.7.2", sha256="dc1246c4e6d168ea4d6e042cfba577c1acd65feea27e56f5ff37df920c30cae0")
    version("3.7.1", sha256="449a5bce64dbd4d5b9517ebd1a1248ed197add6ad27934478976fd5f1f9330e1")
    version("3.6.1", sha256="28ee98ec40427d41a45673847db7a905b59ce9243bb866eaf59dce0f58aaef11")
    version("3.6.0", sha256="fd05ed40cc40ef9ef99fac7b0ece2e0b871858a82feade48546f5d2940147670")
    version("3.5.2", sha256="92d8410d3d981bb881dfff2aed466da55a58d34c7390d50449aa59b32bb5e62a")
    version("3.5.1", sha256="93d651a754bcf6f0124669646391dd5774c0fc4d407c384e3ae76ef9a60477e8")
    version("3.5.0", sha256="92c83ad8a4fd6224cf6319a60b399854f55b38ebe9d297c942408b792b1a9efa")
    version("3.4.3", sha256="b73f8c1029611df7ed81796bf5ca8ba0ef41c6761132340c73ffe42704f980fa")
    version("3.4.0", sha256="a5b82bf6ace6c481cdb911fd5d372a302740cbefd387e05297cb37f7468d1cea")
    version("3.3.1", sha256="cd65022c6a0707f1c7112f99e9c981677fdd5518f7ddfa0f778d4cee7113e3d6")
    version("3.1.0", sha256="8bdc3fa3f2da81bc10c772a6b64cc9052acc2901d42e1e1b2588b40df224aad9")
    version("3.0.2", sha256="6b4ea61eadbbd9bec0ccb383c29d1f4496eacc121ef7acf37c7a24777805693e")
    version("2.8.10.2", sha256="ce524fb39da06ee6d47534bbcec6e0b50422e18b62abc4781a4ba72ea2910eb1")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516
    patch("cmake-revert-findmpi-link-flag-list.patch", when="@3.15.0")

    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873
    patch("cmake-macos-add-coreservices.patch", when="@3.11.0:3.13.3")

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    patch(
        "fix-xlf-ninja-mr-4075.patch",
        sha256="42d8b2163a2f37a745800ec13a96c08a3a20d5e67af51031e51f63313d0dedd1",
        when="@3.15.5",
    )

    depends_on("ninja", when="platform=windows")

    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant("ownlibs", default=True, description="Use CMake-provided third-party libraries")
    variant(
        "doc",
        default=False,
        description="Enables the generation of html and man page documentation",
    )
    variant(
        "ncurses",
        default=sys.platform != "win32",
        description="Enables the build of the ncurses gui",
    )

    # See https://gitlab.kitware.com/cmake/cmake/-/issues/21135
    conflicts(
        "%gcc platform=darwin",
        when="@:3.17",
        msg="CMake <3.18 does not compile with GCC on macOS, "
        "please use %apple-clang or a newer CMake release. "
        "See: https://gitlab.kitware.com/cmake/cmake/-/issues/21135",
    )

    # Vendored dependencies do not build with nvhpc; it's also more
    # transparent to patch Spack's versions of CMake's dependencies.
    conflicts("+ownlibs %nvhpc")

    # Use Spack's curl even if +ownlibs, since that allows us to make use of
    # the conflicts on the curl package for TLS libs like OpenSSL.
    # In the past we let CMake build a vendored copy of curl, but had to
    # provide Spack's TLS libs anyways, which is not flexible, and actually
    # leads to issues where we have to keep track of the vendored curl version
    # and its conflicts with OpenSSL.
    depends_on("curl")

    # When using curl, cmake defaults to using system zlib too, probably because
    # curl already depends on zlib. Therefore, also unconditionaly depend on zlib.
    depends_on("zlib-api")

    with when("~ownlibs"):
        depends_on("expat")
        # expat/zlib are used in CMake/CTest, so why not require them in libarchive.
        for plat in ["darwin", "cray", "linux"]:
            with when("platform=%s" % plat):
                depends_on("libarchive@3.1.0: xar=expat compression=zlib")
                depends_on("libarchive@3.3.3:", when="@3.15.0:")
                depends_on("libuv@1.0.0:1.10", when="@3.7.0:3.10.3")
                depends_on("libuv@1.10.0:1.10", when="@3.11.0:3.11")
                depends_on("libuv@1.10.0:", when="@3.12.0:")
                depends_on("rhash", when="@3.8.0:")
                depends_on("jsoncpp build_system=meson", when="@3.2:")

    depends_on("ncurses", when="+ncurses")

    with when("+doc"):
        depends_on("python@2.7.11:", type="build")
        depends_on("py-sphinx", type="build")

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch("intel-c-gnu11.patch", when="@3.6.0:3.6.1")

    # Cannot build with Intel again, should be fixed in 3.17.4 and 3.18.1
    # https://gitlab.kitware.com/cmake/cmake/-/issues/21013
    patch("intel-cxx-bootstrap.patch", when="@3.17.0:3.17.3,3.18.0")

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch("nag-response-files.patch", when="@3.7:3.12")

    # Cray libhugetlbfs and icpc warnings failing CXX tests
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4698
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4681
    patch("ignore_crayxc_warnings.patch", when="@3.7:3.17.2")

    # The Fujitsu compiler requires the '--linkfortran' option
    # to combine C++ and Fortran programs.
    patch("fujitsu_add_linker_option.patch", when="%fj")

    # Remove -A from the C++ flags we use when CXX_EXTENSIONS is OFF
    # Should be fixed in 3.19.
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025
    patch("pgi-cxx-ansi.patch", when="@3.15:3.18")

    # Adds CCE v11+ fortran preprocessing definition.
    # requires Cmake 3.19+
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5882
    patch(
        "5882-enable-cce-fortran-preprocessing.patch",
        sha256="b48396c0e4f61756248156b6cebe9bc0d7a22228639b47b5aa77c9330588ce88",
        when="@3.19.0:3.19",
    )

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts("%intel", when="@3.11.0:3.11.4")
    conflicts("%intel@:14", when="@3.14:", msg="Intel 14 has immature C++11 support")

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v3.21/cmake-3.21.2-windows-x86_64.zip",
        checksum="213a4e6485b711cb0a48cbd97b10dfe161a46bfe37b8f3205f47e99ffec434d2",
        placement="cmake-bootstrap",
        when="@3.0.2: platform=windows",
    )

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip",
        checksum="8b9b520f3372ce67e33d086421c1cb29a5826d0b9b074f44a8a0304e44cf88f3",
        placement="cmake-bootstrap",
        when="@:2.8.10.2 platform=windows",
    )

    phases = ["bootstrap", "build", "install"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"cmake.*version\s+(\S+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.compiler.name == "fj":
            cxx11plus_flags = (self.compiler.cxx11_flag, self.compiler.cxx14_flag)
            cxxpre11_flags = self.compiler.cxx98_flag
            if any(f in flags for f in cxxpre11_flags):
                raise ValueError("cannot build cmake pre-c++11 standard")
            elif not any(f in flags for f in cxx11plus_flags):
                flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def bootstrap_args(self):
        spec = self.spec
        args = []
        self.generator = make

        # The Intel compiler isn't able to deal with noinline member functions of
        # template classes defined in headers.  As such it outputs
        #   warning #2196: routine is both "inline" and "noinline"
        # cmake bootstrap will fail due to the word 'warning'.
        if spec.satisfies("%intel@:2021.6.0"):
            args.append("CXXFLAGS=-diag-disable=2196")

        if self.spec.satisfies("platform=windows"):
            args.append("-GNinja")
            self.generator = ninja

        if not sys.platform == "win32":
            args.append("--prefix={0}".format(self.prefix))

            jobs = spack.build_environment.get_effective_jobs(
                make_jobs,
                parallel=self.parallel,
                supports_jobserver=self.generator.supports_jobserver,
            )
            if jobs is not None:
                args.append("--parallel={0}".format(jobs))

            if "+ownlibs" in spec:
                # Build and link to the CMake-provided third-party libraries
                args.append("--no-system-libs")
            else:
                # Build and link to the Spack-installed third-party libraries
                args.append("--system-libs")

                # cppdap is a CMake package, avoid circular dependency
                if spec.satisfies("@3.27:"):
                    args.append("--no-system-cppdap")

            # Whatever +/~ownlibs, use system curl.
            args.append("--system-curl")
            args.append("--no-qt-gui")

            if "+doc" in spec:
                args.append("--sphinx-html")
                args.append("--sphinx-man")

            # Now for CMake arguments to pass after the initial bootstrap
            args.append("--")
        else:
            args.append("-DCMAKE_INSTALL_PREFIX=%s" % self.prefix)

        args.extend(
            [
                f"-DCMAKE_BUILD_TYPE={self.spec.variants['build_type'].value}",
                # Install CMake correctly, even if `spack install` runs
                # inside a ctest environment
                "-DCMake_TEST_INSTALL=OFF",
                f"-DBUILD_CursesDialog={'ON' if '+ncurses' in spec else 'OFF'}",
            ]
        )

        # Make CMake find its own dependencies.
        rpaths = spack.build_environment.get_rpaths(self)
        prefixes = spack.build_environment.get_cmake_prefix_path(self)
        args.extend(
            [
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON",
                "-DCMAKE_INSTALL_RPATH={0}".format(";".join(str(v) for v in rpaths)),
                "-DCMAKE_PREFIX_PATH={0}".format(";".join(str(v) for v in prefixes)),
            ]
        )

        return args

    def cmake_bootstrap(self):
        exe_prefix = self.stage.source_path
        relative_cmake_exe = os.path.join("cmake-bootstrap", "bin", "cmake.exe")
        return Executable(os.path.join(exe_prefix, relative_cmake_exe))

    def bootstrap(self, spec, prefix):
        bootstrap_args = self.bootstrap_args()
        if sys.platform == "win32":
            bootstrap = self.cmake_bootstrap()
            bootstrap_args.extend(["."])
        else:
            bootstrap = Executable("./bootstrap")
        bootstrap(*bootstrap_args)

    def build(self, spec, prefix):
        self.generator()

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Some tests fail, takes forever
        self.generator("test")

    def install(self, spec, prefix):
        self.generator("install")

        if spec.satisfies("%fj"):
            for f in find(self.prefix, "FindMPI.cmake", recursive=True):
                filter_file("mpcc_r)", "mpcc_r mpifcc)", f, string=True)
                filter_file("mpc++_r)", "mpc++_r mpiFCC)", f, string=True)
                filter_file("mpifc)", "mpifc mpifrt)", f, string=True)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before cmake packages's install() methods."""

        module.cmake = Executable(self.spec.prefix.bin.cmake)
        module.ctest = Executable(self.spec.prefix.bin.ctest)

    @property
    def libs(self):
        """CMake has no libraries, so if you ask for `spec['cmake'].libs`
        (which happens automatically for packages that depend on CMake as
        a link dependency) the default implementation of ``.libs` will
        search the entire root prefix recursively before failing.

        The longer term solution is for all dependents of CMake to change
        their deptype. For now, this returns an empty set of libraries.
        """
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])

    def run_version_check(self, bin):
        """Runs and checks output of the installed binary."""
        exe_path = join_path(self.prefix.bin, bin)
        if not os.path.exists(exe_path):
            raise SkipTest(f"{exe} is not installed")

        exe = which(exe_path)
        out = exe("--version", output=str.split, error=str.split)
        assert f"version {self.spec.version}" in out

    def test_ccmake(self):
        """check version from ccmake"""
        self.run_version_check("ccmake")

    def test_cmake(self):
        """check version from cmake"""
        self.run_version_check("cmake")

    def test_cpack(self):
        """check version from cpack"""
        self.run_version_check("cpack")

    def test_ctest(self):
        """check version from ctest"""
        self.run_version_check("ctest")
