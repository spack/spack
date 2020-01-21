# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gradle(Package):
    """Gradle is an open source build automation system that builds
    upon the concepts of Apache Ant and Apache Maven and introduces
    a Groovy-based domain-specific language (DSL) instead of the XML
    form used by Apache Maven for declaring the project configuration.
    Gradle uses a directed acyclic graph ("DAG") to determine the
    order in which tasks can be run."""

    homepage = "https://gradle.org"
    url      = "https://services.gradle.org/distributions/gradle-3.4-all.zip"

    version('4.8.1', sha256='ce1645ff129d11aad62dab70d63426fdce6cfd646fa309dc5dc5255dd03c7c11')
    version('3.4',    sha256='37c2fdce55411e4c89b896c292cae1f8f437862c8433c8a74cfc3805d7670c0a')
    version('3.3',    sha256='71a787faed83c4ef21e8464cc8452b941b5fcd575043aa29d39d15d879be89f7')
    version('3.2.1',  sha256='0209696f1723f607c475109cf3ed8b51c8a91bb0cda05af0d4bd980bdefe75cd')
    version('3.2',    sha256='e25ff599ff268182b597c371ed94eb3c225496af5d4e7eb9dcbb08d30f93a9ec')
    version('3.1',    sha256='43be380834a13e28e9504c21f67fe1a8895ab54f314a6596601896dca7213482')
    version('3.0',    sha256='9c8b7564ea6a911b5b9fcadd60f3a6cea4238413c8b1e1dd14400a50954aab99')
    version('2.14.1', sha256='88a910cdf2e03ebbb5fe90f7ecf534fc9ac22e12112dc9a2fee810c598a76091')
    version('2.14',   sha256='65bbc0ef9c48be86fb06522fc927d59dcc7c04266f2bb8156be76971f7c3fc4a')
    version('2.13',   sha256='fb126ed684150f9dc39a811cbcf4daada4292fd387ed998c151ff2cf2536d94d')
    version('2.12',   sha256='d8b1948a575dc9ec13e03db94502ce91815d73da023f611296c04b852164cb5f')
    version('2.11',   sha256='a1242e4db8f979998796b1844e608c2acf8f8f54df518bbb3d5954e52253ba71')
    version('2.10',   sha256='496d60c331f8666f99b66d08ff67a880697a7e85a9d9b76ff08814cf97f61a4c')
    version('2.9',    sha256='4647967f8de78d6d6d8093cdac50f368f8c2b8038f41a5afe1c3bce4c69219a9')
    version('2.8',    sha256='65f3880dcb5f728b9d198b14d7f0a678d35ecd33668efc219815a9b4713848be')
    version('2.7',    sha256='2ba0aaa11a3e96ec0af31d532d808e1f09cc6dcad0954e637902a1ab544b9e60')
    version('2.6',    sha256='5489234fc9c9733fc4115055618763ccb4d916d667980e6ab4fa57fc81197d16')
    version('2.5',    sha256='b71ab21fa5e91dcc6a4bd723b13403e8610a6e1b4b9d4b314ff477820de00bf9')
    version('2.4',    sha256='371cb9fbebbe9880d147f59bab36d61eee122854ef8c9ee1ecf12b82368bcf10')
    version('2.3',    sha256='515962aeec8c3e67b97f0c13c4575beeed1b5da16181d8b9054416339edc8c2d')
    version('2.2.1',  sha256='1d7c28b3731906fd1b2955946c1d052303881585fc14baedd675e4cf2bc1ecab')
    version('2.2',    sha256='65fc05f787c7344cc8834dc13a445c91ea3712a987f5958b8489422484d7371b')
    version('2.1',    sha256='b351ab27da6e06a74ba290213638b6597f2175f5071e6f96a0a205806720cb81')
    version('2.0',    sha256='11c32ed95c0ed44e091154391d69008ac5ec25ad897bc881547e6942a03aeb13')
    version('1.12',   sha256='cf111fcb34804940404e79eaf307876acb8434005bc4cc782d260730a0a2a4f2')
    version('1.11',   sha256='07e58cd960722c419eb0f6a807228e7179bb43bc266f390cde4632abdacdd659')
    version('1.10',   sha256='cd1a0f532258369c414a56b3e73b7bd7f087cf515b7c71dcb9091598c4a8d815')
    version('1.9',    sha256='eeb919fe734bc4a63aaf75c05c19bc55c8bccc925b0eca4269c67f7e8cf48efb')
    version('1.8',    sha256='4f03076116841743808c2f2c1ae2041d03adebe09ab80356b87516c7ed055e40')
    version('1.5',    sha256='fecf73744c5695e2a3078104072ae2a9fdec17e36dc058dc20adf8c7be8af13b')
    version('1.4',    sha256='436771c854cc665c790a6c452a2878dfbdaaf9d14e505a58127b407bb05b013f')
    version('1.3',    sha256='c8572e9579e2300c5e2e8ae8f1a2433d9fd7ad9a4b1e721a5ee588c72fbf7799')
    version('1.2',    sha256='ea66177dd532da09cb28d050e880961df5bd7ba014eda709c76f2c022f069282')
    version('1.1',    sha256='00519a961f7f902123368c5bfe4c01be607628410620c8c8a466fbb0de8c6715')
    version('1.0',    sha256='510258aa9907a8b406a118eed1f57cfe7994c4fe0a37a6f08403fe3620526504')
    version('0.9.2',  sha256='a9b33c1cb7c056a7bd26b588301ce80f0b6e3872d18b0f1cb80ab74af0e62404')
    version('0.9.1',  sha256='6b9e2033e856ed99b968d71c2dc5174dc5637c10d5e4cc9502a51e86f45709eb')
    version('0.9',    sha256='a06117e826ea8713f61e47b2fe2d7621867c56f4c44e4e8012552584e08b9c1b')
    version('0.8',    sha256='42e0db29f2e0be4eeadfe77b6491d9e2b21b95abb92fc494dfcf8615f2126910')
    version('0.7',    sha256='ca902f52f0789ab94762f7081b06461f8d3a03540ab73bf2d642f2d03e8558ef')

    depends_on('java')

    def install(self, spec, prefix):
        install_tree('.', prefix)
