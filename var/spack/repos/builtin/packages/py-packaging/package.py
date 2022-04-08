# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class PyPackaging(PythonPackage):
    """
    Reusable core utilities for various Python Packaging interoperability specifications.
    """

    homepage = "https://github.com/pypa/packaging"
    pypi = "packaging/packaging-21.3.tar.gz"

    version('21.3', sha256='dd47c42927d89ab911e606518907cc2d3a1f38bbd026385970643f9c5b8ecfeb')
    version('21.2', sha256='096d689d78ca690e4cd8a89568ba06d07ca097e3306a4381635073ca91479966')
    version('21.1', sha256='cb730b9a81a64c88b1058ab094e6e7539a82aded6c6a578e0173ae31ad47592a')
    version('21.0', sha256='7dc96269f53a4ccec5c0670940a4281106dd0bb343f47b7471f779df49c2fbe7')
    version('20.9', sha256='5b327ac1320dc863dca72f4514ecc086f31186744b84a230374cc1fd776feae5')
    version('20.8', sha256='78598185a7008a470d64526a8059de9aaa449238f280fc9eb6b13ba6c4109093')
    version('20.7', sha256='05af3bb85d320377db281cf254ab050e1a7ebcbf5410685a9a407e18a1f81236')
    version('20.6', sha256='3f604d302b77be0ce21d38c75e2dc18ed3d466e3861baafd2cfa32735ec1bc85')
    version('20.5', sha256='5d21ed3d936beb102850195eadaa1371bfb4b93da6ad63d231410c6dca25a665')
    version('20.4', sha256='4357f74f47b9c12db93624a82154e9b120fa8293699949152b22065d556079f8')
    version('20.3', sha256='3c292b474fda1671ec57d46d739d072bfd495a4f51ad01a055121d81e952b7a3')
    version('20.2', sha256='e725568545a15ce87ff23631ddacb9f3f4c398031d5faa7b7d01738a9ee0b0e0')
    version('20.1', sha256='e665345f9eef0c621aa0bf2f8d78cf6d21904eef16a93f020240b704a57f1334')
    version('20.0', sha256='fe1d8331dfa7cc0a883b49d75fc76380b2ab2734b220fbb87d774e4fd4b851f8')
    version('19.2', sha256='28b924174df7a2fa32c1953825ff29c61e2f5e082343165438812f00d3a7fc47')
    version('19.1', sha256='c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe')
    version('19.0', sha256='0c98a5d0be38ed775798ece1b9727178c4469d9c3b4ada66e8e6b7849f8732af')
    version('18.0', sha256='0886227f54515e592aaa2e5a553332c73962917f2831f1b0f9b9f4380a4b9807')
    version('17.1', sha256='f019b770dd64e585a99714f1fd5e01c7a8f11b45635aa953fd41c689a657375b')
    version('17.0', sha256='e9f654a6854321ac39d2e6745b820773ba9efa394e71dea1b387cc717d439f93')
    version('16.8', sha256='5d50835fdf0a7edf0b55e311b7c887786504efea1177abd7e69329a8e5ea619e')
    version('16.7', sha256='2e246cde53917a320c4edb549b6b6ed0c80e22be835047bad814687c7345011e')
    version('16.6', sha256='a335d0778b77d3525875dfe66c2b880529e3bbde08e1a6604710ac36f851021a')
    version('16.5', sha256='b763bd2a025e957323f761bf00fb72e8c17ac1c6d5eb8fb55c18802f2143f911')
    version('16.4', sha256='325db5b475511303f17e96047877bfc6ba9c895b6850df4a98d95bfbc0329cb1')
    version('16.3', sha256='46e5808cdfd3766d41d3691d413ca3515bd060f16fca5aab080d5a6a204ec33c')
    version('16.2', sha256='0eb4a6329c6d40a0deef725b4f510b6219ec8c365f888583babbb4454d761dd6')
    version('16.1', sha256='7792caf5bfda630c96310a84ecba5d61b17a843ab72194bb5606d81e4f44094f')
    version('16.0', sha256='a32895134cd7b86ee8add60a3be5bfd7ef3f30e73e5b54221dbe67d0e0690689')
    version('15.3', sha256='1e9a6b9ad621bc1dbd3aa8dfff52abc4b44f5c14fbb406731c25cba250a5f61e')
    version('15.2', sha256='cf92396a51d269eb10660367c7c40cea1aa3180a6a3a773d377cf7451007c6fe')
    version('15.1', sha256='9f4fad6c70b47aee71ba8b2b17a9f610b32abad84be99b7d3d940748bce4b1f0')
    version('15.0', sha256='6f6cfaf59a40cfba8ee8cf734d8a544e0731bbaa1163ab04e7652b25af256deb')
    version('14.5', sha256='363f9193daa14085b8dfeeb2bf64227bcf1dc85c02ae2a5c6018b01f77e46491')
    version('14.4', sha256='fee2bcfc2dccf09c9fff14a4a9e8bc8114b581f5daedf2517c9505e0e693e2ab')
    version('14.3', sha256='4f0bf96d626042d964ead1572f8a89603416d5a5c8284a7968dd1de26ba9a13b')
    version('14.2', sha256='236efc871728034662f265aa8c590f3cc3aa8cb2f86112402ff012dbb27622f8')
    version('14.1', sha256='74b388a679d59a37802a1553bbf561fc8359487f074b0c57eb334e53f1ca7982')
    version('14.0', sha256='89f36ecd68941f59e1447796b6068d403151a0338804bd2ed65313517fde1ea2')
