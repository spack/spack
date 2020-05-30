# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetkitFtp(AutotoolsPackage):
    """The standard UNIX FTP (File Transfer Protocol) client."""

    homepage = "http://ftp.linux.org.uk/pub/linux/Networking/netkit/"
    url      = "http://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-ftp-0.17.tar.gz"

    version('0.17', sha256='61c913299b81a4671ff089aac821329f7db9bc111aa812993dd585798b700349')

#    parallel = False

    depends_on('readline')
    depends_on('ncurses')

    patch('netkit-ftp-0.17-pre20000412.pasv-security.patch', sha256='edfd2f7636dfc156b544895fd82d93116fdce82728c1945c8e43ecdf1e67c8b6')
    patch('netkit-ftp-0.17-acct.patch', sha256='892610782802f789bced600154d5211bdce334290700e5d0bb96c32798348ba2')
    patch('netkit-ftp.usagi-ipv6.patch', sha256='ecbc92594f77c3ae22a4d284a0abe4bfcf51c40e8d5731f6f9997fe6667e6404')
    patch('netkit-ftp-0.17-segv.patch', sha256='ff54caec26085e97932969307f318ff8c25e256266388049e81afb40fcd2a94c')
    patch('netkit-ftp-0.17-volatile.patch', sha256='6842009651d85dbb6d7c550d5369043d817cfb08c9859cc42f0debf2b1a0c3e3')
    patch('netkit-ftp-0.17-runique_mget.patch', sha256='12be7c13ce3e32bf722ae7290ed4053a2270a67b4c8effb79b9043ec4eae9c86')
    patch('netkit-ftp-locale.patch', sha256='2ae34e69c63379cd437cf79c872afb95d98c17bcca1c8fc9bae0ad72415304ed')
    patch('netkit-ftp-0.17-printf.patch', sha256='36576937907b221e85b5d78924fc9730bc7bfb183404469054611b19e399110b')
    patch('netkit-ftp-0.17-longint.patch', sha256='f8fe86e393dddc7ee7af5c7d40c73530be0cc8c8e77247298d6d1289e2ad77b8')
    patch('netkit-ftp-0.17-vsftp165083.patch', sha256='df1e9af7903bc44cf4e6189d143f5bc4c5fbe7cfc9c7bf9e58e77dbc16cc3910')
    patch('netkit-ftp-0.17-C-Frame121.patch', sha256='b4429406e37346cc73898ac926cdcdcad00d569dabf15a2751916042c17f08d6')
    patch('netkit-ftp-0.17-data.patch', sha256='89d8a4a1e7dd3075e6f8880229eeb5a555b1da97c94a52ec933bfff087dd3b71')
    patch('netkit-ftp-0.17-multihome.patch', sha256='1777b65e8257f5df0ad75f83b8dc879f364c86dc4ea3b9d0ace65e6bd5e56503')
    patch('netkit-ftp-0.17-longnames.patch', sha256='58775b4c5d141239904ec325c8d57fd6b48041a109affb606922e94662a1b114')
    patch('netkit-ftp-0.17-multiipv6.patch', sha256='e9a0b15f9850bb4bf43b44a1d24dc50460911a03a81688af9875bdd0c9b5c4ea')
    patch('netkit-ftp-0.17-nodebug.patch', sha256='13cbd40cbcc5f371a3de9bfa2db389efebf9f170359e805402221d4bd6744f97')
    patch('netkit-ftp-0.17-stamp.patch', sha256='3edab6bfeb2eaa548f5f4913a51ff51e6faa4f80b74371754334f110d72ea1e6')
    patch('netkit-ftp-0.17-sigseg.patch', sha256='f8ece2c062220c72c2c2b0740bbf8291f211ab9e7c6cd839319b6373febc15a0')
    patch('netkit-ftp-0.17-size.patch', sha256='6658d955acfb835ce8f0a6f4a774522735d37e370349e548c40a13175f88114a')
    patch('netkit-ftp-0.17-fdleak.patch', sha256='982a771ff3ea66f5bbd9d2650512a35aafb324ca2b704757826089746be40806')
    patch('netkit-ftp-0.17-fprintf.patch', sha256='93840645b583e42f14954ff9e8ec5d8374b9c8992d1cf7705abc5536797871f6')
    patch('netkit-ftp-0.17-bitrate.patch', sha256='9cd6f881ff888e59c5eeb44cc6e092d48177a08f69c2d3f2676d6a67d03d9c35')
    patch('netkit-ftp-0.17-arg_max.patch', sha256='e38bd3d24923839b0409989063ec61753fe9c52e08ea4d3ec3f347c6103a46b3')
    patch('netkit-ftp-0.17-case.patch', sha256='0023b5096863a6ecaf89d92a599507d45b14414d0bbe4b2b59c60aaabcb22cc3')
    patch('netkit-ftp-0.17-chkmalloc.patch', sha256='e6ccfa3c3f1aa3f2b53823a58acc5dd48c47640c67ca075e98c809633f840770')
    patch('netkit-ftp-0.17-man.patch', sha256='44dcd22c41f71968819c84ef4596781a903949f500e479e250d25ac9f1684860')
    patch('netkit-ftp-0.17-acct_ovl.patch', sha256='ba80bf071ee87788afd0e5c8928ccf8fa8d3e13a0ee09deadbbb67f597642098')
    patch('netkit-ftp-0.17-remove-nested-include.patch', sha256='5f218a76516ba5e3274d0e0c188f4234d0a952afa673f7d12e8d33251b1805a6')
    patch('netkit-ftp-0.17-linelen.patch', sha256='476c32040df648a353ec5406654effcaad60134c979f927fbb1d8925c8b3ba50')
    patch('netkit-ftp-0.17-active-mode-option.patch', sha256='bfc98e1f440138ced582568ecde488359c55edf803234171cc58ff473cde4749')
    patch('netkit-ftp-0.17-commands-leaks.patch', sha256='d93f72192fdb46b9cab39c704dbee52bb7a036658d7b8690790a517aa9a9d0de')
    patch('netkit-ftp-0.17-lsn-timeout.patch', sha256='ebd4f7ead187b6c13cb309da2b54bc98149d28875ab091eccd804db0cb5de06d')
    patch('netkit-ftp-0.17-getlogin.patch', sha256='e0024406c9d7a92415ed27620046cb99cc882d4c29a17791c61ab3bd5e215ef2')
    patch('netkit-ftp-0.17-token.patch', sha256='df7fbe869306bc064ec389c24b9580fe08a81e6bb8d31c35430b3d41f4f89839')

    def configure_args(self):
        config_args = [
            '--enable-ipv6'
        ]
        return config_args
