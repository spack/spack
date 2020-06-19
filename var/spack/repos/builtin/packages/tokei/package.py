# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tokei(CargoPackage):
    """Tokei is a program that displays statistics about your code. Tokei will
    show the number of files, total lines within those files and code,
    comments, and blanks grouped by language.
    """

    homepage = "https://github.com/xampprocky/tokei"
    crates_io = "tokei"
    git = "https://github.com/xampprocky/tokei.git"

    # tokei doesn't build with prefer_dynamic at present, so switch default to
    # False
    variant(
        'prefer_dynamic',
        default=False,
        description='Link Rust standard library dynamically'
    )

    variant(
        'json',
        default=False,
        description='Support JSON output'
    )

    variant(
        'yaml',
        default=False,
        description='Support YAML output'
    )

    variant(
        'cbor',
        default=False,
        description='Support CBOR output'
    )

    def cargo_features(self):
        features = []

        for feature in ["json", "yaml", "cbor"]:
            if '+{0}'.format(feature) in self.spec:
                features += [feature]
                
        return features

    version('master', branch='master')
    version('11.2.1', sha256='e3ef140433084bf29e91d95bf003ba4f73809728f315e81bba63f7928a8f8547')
    version('11.2.0', sha256='88b739d6420e03fb1b4fc881c457c9e2f6d6c0c3634200e6e53a1eeadad72d33')
    version('11.1.1', sha256='e28e6c319fa1fd848ecb764220c632232ab76872cbf2f70f59f86bf1128d64bf')
    version('11.1.0', sha256='6e8e8cd2f56cd31fc97766f07e2b989c4d774174de804503f53789e689988fe6')
    version('11.0.0', sha256='fa869112e75b141332150e957cb6f29b3b593b8960379ef923b2f7d4918aaa2d')
    version('10.1.2', sha256='3163fd12ef922838fc371ce116a7eeee0c1997fae086133a1a86d0e3cbff7a28')
    version('10.1.1', sha256='35208ab8a5f5e83d6ce64cf967bb9b30b552c54530bdccd11c344dc1b1a2c51d')
    version('10.1.0', sha256='345ad4073d1181397d1090e29f1d35b241059e36a26b96e33c384497e00e33a0')
    version('10.0.1', sha256='11c7f2db6985306d43d5cbccdd39800013bcb766c0ac4d6972c2b1023be29cfe')
    version('10.0.0', sha256='a587e497839fd5e8cf976666c9378b36bede0d5ab7b4a0941a07fbd19970c7e5')
    version('9.1.1',  sha256='c8b3d150636a2618cd82a6ffa8a67ac380566aaf2ca84f6fcf3ba8f83e071bcf')
    version('9.1.0',  sha256='29040a1cb972aa33f8686ea90c96bba911a300c8286e222c5d38108bf9bfb3a7')
    version('9.0.0',  sha256='aaa764e533440c271a962b338d126a36dea64a108a1f1f1a053c56a51cdcdf67')
    version('8.0.1',  sha256='bfdcbacc1767851b4a330ff74f521e20b746954bac282d3928ae300454fb24e2')
    version('7.0.3',  sha256='0cbb78d71756851d97e8708a47a747288102a0283e8ddc413c5569a9ca821a8d')
    version('7.0.2',  sha256='14f460f8c6f00e5a65aaffcb898a2772914c0054a60d02e28e6feaa93e2e03dc')
    version('7.0.1',  sha256='60e6cfd85b7ea05b4f49e0d944eb57afc9a1a26e4eb6c1306acfd43ec8a80a11')
    version('7.0.0',  sha256='d6deaf6bcb9d03a5a6d25e390746c26e8a35d70fc28d8e08c693e60455553cc1')
    version('6.1.3',  sha256='b907e9e1f626a1b2d6981a205a3b0656b8bc2e38a0fd1b84feb2eee3af1bbd1b')
    version('6.1.2',  sha256='de54741943ae426c87e767f6d741373be42afca8de39b3cda8a4b934845f674c')
    version('6.1.0',  sha256='cb0fb4ae46ed6185af04b371954a128b37ea5e9396bca9e0cbddbf38e404bdb9')
    version('6.0.2',  sha256='562df3c899561b5de6fb9837f733cf96801f7876bb4ee135f0e3bfff02d9fdb3')
    version('6.0.1',  sha256='b6bf30ee3aa108fe0be26ba028a310e129ce4ba88ee095ac46a7ede7a90c8980')
    version('6.0.0',  sha256='f86cb74bebb766f529ed09f70b39284e7894d9677124e42a90c9ca230eb0b5be')
    version('5.0.7',  sha256='fc542e2fa50b92c323dab350e421845c51c54520f50a2343db1a81427c6af47d')
    version('5.0.6',  sha256='64adba158bdc288d43598beca62697d054f069bd8a0ac309174d08a091dfbe42')
    version('5.0.5',  sha256='2cf943aa1ba232e1d5393bc1307eaad416d50e802e11152e85511cfa54450d46')
    version('5.0.4',  sha256='68599b4081eaf0c83065204a0d52cd7bf48a8a209f2f7c359d8c02e770c3bb38')
    version('5.0.3',  sha256='53b4e5c49280dd1f971a02c4cfedab9627a66dc909b5e03ee317e4e75da947ff')
    version('5.0.1',  sha256='0d3e1b1afdb637996e4a12a89c5b189f0f91b0ccdde72451d66f5bee78d19f3e')
    version('4.5.4',  sha256='cfdb913211cc33d608d8a5e54c6eb77615ce9141f2abea4d0bb48f047af31b5e')
    version('4.5.3',  sha256='46c1692778e8991cf9ce5405882a304e7217ab979306673020bf607975971b90')
    version('4.5.2',  sha256='09fe2bf5bcfee529ac2ad094248d366c5df9ffb09b3a2a6a55bb00d465a70bf2')
    version('4.4.0',  sha256='7aa034018f9963a31aefd3c2ad99b1c2b47e3693a05aaa98916b157d0dfa082d')
    version('4.3.0',  sha256='eb518b48797acfabc9380fc628cd3fc2a593507012c11a06d6f19be80680d3e1')
    version('4.2.0',  sha256='181899048aa679aa097869bfd74444eac8ee51ec3389135d5b1518c2d05b051d')
    version('4.1.1',  sha256='01cc6be47c5672a4fb0cc7e6d9af02607336e33212a353b14304299df5277a9e')
    version('4.1.0',  sha256='e50b1fd3c3167c209d03a0280cabdd661d6cd604ab834f7253d9ccbb336dedfe')
    version('4.0.0',  sha256='fa53dd8e9762dbdab913ab89fdd88f17a4416b9d3fe969e935fcfce816678a40')
    version('3.0.2',  sha256='b4e55376d38a64e7b3485919b4434a61d2ac51d1ec446d4a27da4c7c213bc20e')
    version('3.0.1',  sha256='4945c3d031a87842a9281b4e8c3f60a9840d75dd5047ad8f275f84b1eb20548f')
    version('3.0.0',  sha256='fba6650fbb0e16c2ac65bd878bb1eca54f1054148253db6a5316894f90d80f6a')
    version('2.1.3',  sha256='7ef21c4ff6bb988ddbf63f2af7202bc503e68a4a7a0b577440d7bfb17cde738c')
    version('2.1.2',  sha256='a00174b0e513cfebd58fa17dfb2c546ca8234b3c4d2ebb95c4292f3f361326fd')
    version('2.1.1',  sha256='c1edb7de2d03b2a0ce46904ab6c75f15a20d01e79bbf206046881fc132409ccd')
    version('2.1.0',  sha256='d844afc07ca43047e10d7b95fbfca66c8c2c3d82601e89f66deac6ed7a94d6de')
    version('2.0.0',  sha256='9134db11b57032d0d0d0e54efa3b7ecb92fda53b46d4a8f47c18e71ba9840ee0')
    version('1.6.0',  sha256='2f7bf4f21069df8c55e0aba24644a615acd30d30d2e670aaaac6c25e86d4bdb9')
    version('1.5.1',  sha256='1b3cb8fb074f04f7e20c1b5917c740fc96c55d2f1fb51c56d6889e76d1eaa16e')
    version('1.5.0',  sha256='5c5f5764dd42d3c0ce6f1060cf7911c9372cc7f92a8734a055042845850016ac')
    version('1.4.1',  sha256='bb99a5d5decede7cdaadd604c5353a2fbce51860fd6fedbacf436a4cd34ff871')
    version('1.4.0',  sha256='d249950eae5e34409b6ff6bdb9e9667969a9586d0e75aebe47d6950fc0d59e9c')
    version('1.3.1',  sha256='e821478d288cebd0be2aa449f043bfef4184465c9e8b70e56ccbfae2660ce206')
    version('1.3.0',  sha256='79f10723adb27c5ff473c03083880dd21aa1e567a36e5077d9c960d781346895')
    version('1.2.1',  sha256='7b9240a2841e2b6dea06d30a892694bba264ee66154532bff37b30a3d1821ff3')
    version('1.2.0',  sha256='882c55670629161425759c96a71d44d6163311c193dcfa15cfd50a97dd59c1b8')