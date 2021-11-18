# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter


class PySerpent(PythonPackage):
    """
    Serialization based on ast.literal_eval
    """

    homepage = "https://github.com/irmen/Serpent"
    pypi = 'serpent/serpent-1.40.tar.gz'
    maintainers = ['liuyangzhuan']

    
    version('1.9', sha256='46311ae0e93c30c3b93e9153ffd6c76e595aaaca9d390f0cda1a750d5957f90f')
    version('1.8', sha256='9bd9adfde5337d839c16a62b7d02b058b3612a1beaccf2dc5f5000656c406336')
    version('1.7', sha256='5345587dff787431df668c19de56b74ada02fb893c2d9687572ffecc63d4d33a')
    version('1.6', sha256='cf4653ad238927775da35afb8fca3ff0c8bc21fe7c88959647883b06e0b1d4cf')
    version('1.5', sha256='c9202089dc07b66ec5a5bca33eb5b745e5caf19b6909185b88439daa4d5840f8')
    version('1.40', sha256='10b34e7f8e3207ee6fb70dcdc9bce473851ee3daf0b47c58aec1b48032ac11ce')
    version('1.4', sha256='dc95871fcf3c11446dc42049c4941f38c6cb67d85e9207d3dcd4b904a59805f0')
    version('1.30.2', sha256='72753820246a7d8486e8b385353e3bbf769abfceec2e850fa527a288b084ff7a')
    version('1.30.1', sha256='34070629becc4db10ff35ddcaed0f6ab83135fff0a6bd3b913910656bba0eb64')
    version('1.30', sha256='74af57fdc2a5f69b2f5702c6ecc71815d1b6a0505690430407302b1727d50d59')
    version('1.3', sha256='45560ada9e07e1400304870210c64c2de14ab414e23ec7a1271d673fa92104e2')
    version('1.28', sha256='f306336ca09aa38e526f3b03cab58eb7e45af09981267233167bcf3bfd6436ab')
    version('1.27', sha256='6f8dc4317fb5b5a9629b5e518846bc9fee374b8171533726dc68df52b36ee912')
    version('1.26', sha256='26116545d6ea12d9ea567e38fa440930f2ae79cd72e4633b8302e93d9d7af887')
    version('1.25', sha256='264a028e059c1b557701ae7c567cdab330dbd228ff924489343efcb39bd828a0')
    version('1.24', sha256='b6855483d95a03b6aee358363684cd38a3a670240da5bc6da4253079cb07b8df')
    version('1.23', sha256='8480ce3d8864b8974d9fe396998c6a7dae96edb68edf905bfd32ea9a11853ba5')
    version('1.22', sha256='a67ca57082b00ea734854d751ab19e8a49d4ea0d4be7194985da35863fb9fb19')
    version('1.21', sha256='db76814fe33b25acec2748ae124380bddeba0605dee29c5470b078fb1573ff0e')
    version('1.20', sha256='7f7cf387cabc14b8a881a7910efc46c92b548423c4095d5b9e7cc1c9e48be143')
    version('1.2', sha256='e233c7526715d08c3ef0a872f6f3e5a44097f58a557f635af67c91246d5c9841')
    version('1.19', sha256='946b2c837f889971df3575af9dadd8f09bfe48549ebc1b9f6434263b653707ce')
    version('1.18.1', sha256='9afebb58ac8b827050e1969324388349dc9738b0a03b0d91567b328834a27732')
    version('1.18', sha256='cc4e1aff3a38a0d438526bede81480776fa8c33fa6d5059412988b0754c9af6d')
    version('1.17', sha256='1fa1c0eabc179fa47815beaed1910571f05cdaccaa696ff1e237da751aa2bfd6')
    version('1.16', sha256='c26e98c2155228a69eb0dc14ba7b888cb70099b6c4ca47fd9d1f099f7d561c3e')
    version('1.15', sha256='f5bc2cd19b79e7ac0821cc8278c4be7a69b2eef07d96f3c6f7977e14b2098c79')
    version('1.14', sha256='6493009325af134ee7c5bbf57ce1a16b07b6694982e0657340645bf225eaf841')
    version('1.13', sha256='32941d185e28249a7babc754ab7df9c9808e1d5d3cdbf3c461aba9790e710a9e')
    version('1.12', sha256='1221fc402ab7aa3c3bac85a27e30df2c08658c7bf7a20e8d0025a10edc1788c0')
    version('1.11', sha256='ab5df8f28574552bdbaf8d3774e6d0faff62f0aa6d5e6bb33b6b0c46937001ad')
    version('1.10', sha256='06f4863c1b2ace6871dcbf69f74d50a08afc8bd427445d1f5c59b03d976e204b')
    version('1.1', sha256='e55079b8e47a61ca555f72f0b918ca5e0fb6c6e6353492ec7d818be4c04da133')
    version('1.0', sha256='87524ec3842d69e45850b13acdf53bd52286d209bba48e078f31c5a4ff616bb6')

    depends_on('py-setuptools', type='build')
