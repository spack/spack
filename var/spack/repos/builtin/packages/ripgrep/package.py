# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ripgrep(CargoPackage):
    """ripgrep is a line-oriented search tool that recursively searches
    your current directory for a regex pattern.  ripgrep is similar to
    other popular search tools like The Silver Searcher, ack and grep.
    """

    homepage = "https://github.com/BurntSushi/ripgrep"

    # Pull ripgrep directly from crates.io for published releases
    crates_io = "ripgrep"
    # Can install master branch from GitHub
    git = "https://github.com/BurntSushi/ripgrep.git"

    version('master', branch='master')

    # Crates.io working versions
    version('12.0.1', sha256='7dc6e92652933ac66d236d78ef61658b73c09639981bd1be0630461ce64d3cab')
    version('12.0.0', sha256='117f3608a82950b647d8f158cbd3388bffc0a594f29b2c39198392134126b6c0')
    version('11.0.2', sha256='d903146d825e92f77f95d1e1e8e5272f42253978c07d58c2294467a14dca126f')
    version('11.0.1', sha256='bafda49e418a8cd7df1fddddab809beb131117c698dc120ca614019b3e05c42e')
    version('11.0.0', sha256='486a3ec7c145d02ede421326b9d699a6d0ab090ea443ca7a888a64b859652a10')
    version('0.10.0', sha256='7f3ab77309993175ac2fe01a7f990bf972c0ddae0d63d747693d598bfaf2de44')
    version('0.9.0',  sha256='fe3cebe7e44dc53484fe207c3355a727c6b299feb335bd7ef2ea5dd0ebe9e5d6')

    # These versions have incomplete crates.io listings (`Config.toml` is to
    # a relative path), but still successfully build from Git.
    version('0.5.2',  commit='91215019096ba16b0aba610fcffc01a055010c04')
    version('0.5.1',  commit='3a23993ce30564b79af6fd5a6bd92543804efaca')
    version('0.5.0',  commit='06d9c929a0ed279a403debea4394a948197a7e8b')
    version('0.4.0',  commit='bf78d26bc14d9775f57238cfc4129a7635b05856')
    version('0.3.2',  commit='df0fb665455ca8f0e6ffc512805cde8b9332a683')

    # These versions do not build due to dependencies which no longer build.
    # version('0.8.1',  sha256='c2ac58be506de28e3e85143dd107f3406c8b2c3d528cb28158bda8928d39e429')
    # version('0.8.0',  sha256='0a8566ba56927c60657ea2012f0d4acfcc277485f249de7d7c9e6a202ce30736')
    # version('0.7.1',  sha256='811c00a85f41a52172b955145d8119aaeb1e28a23e651ac22559668ad92959e5')
    # version('0.7.0',  sha256='9dffa23b3db2c8e7012775852069d3e36d99928055dbaab7cab29fad2b6fc2da')

    # These versions have incomplete crates.io listings, and have build issues
    # today.
    # version('0.6.0',  commit='821f9d3073c606d7cafd9a121a7b5a9c47bf8cd7')
    # version('0.3.1',  commit='8540a37e8cdd9b894259127764a36412b035e365')
    # version('0.3.0',  commit='448e41407ff6ae339f2fe96949cddb90354277da')
    # version('0.2.9',  commit='3fd5d4afc6320c41c0b80b8753be175fb97d6e1a')
    # version('0.2.8',  commit='34995b40fe9ca02cf2b44aec140a9852f4c25566')
    # version('0.2.7',  commit='5654657c77e877eb772078b434bb4b877afa0110')
    # version('0.2.6',  commit='3f406f93b8fde9eef4f8ee94766d134df365d207')
    # version('0.2.5',  commit='624c47579aca24c23785dd620cd3ba8bf57ae106')
    # version('0.2.4',  commit='7ef4b45e79606e63d0dac1f139fe87632427fb06')
    # version('0.2.3',  commit='dd38020660ac2bdb0f74669186bac5d9297ffa41')
    # version('0.2.2',  commit='7cb2a3c404851775f9cfb45ac6614babde0c28c1')
    # version('0.2.1',  commit='928c2cfd1fef428f6c9e0eb033f1c134227ee1a7')
    # version('0.2.0',  commit='c256ed1b7572386050bd1cc968d2480fbd6e840f')
    # version('0.1.17', commit='afe242e071f01c0426ed3a022cf6c65d443dc30d')
    # version('0.1.16', commit='95e927e945472694aafc9fb4fdb447b882457d6c')
    # version('0.1.15', commit='f3c2b645165ab71d71ce06725a9899f6c01c4050')
    # version('0.1.14', commit='a8e93c0d52e328fca2615ed9a424fc49373a4f74')
    # version('0.1.13', commit='9c5f593d2510ea0e587f74b713e4f59031aa03f4')
    # version('0.1.12', commit='31027a417b3870c7e6ec6a034d485edaaa7e78ed')
    # version('0.1.11', commit='173a519aa498f6ce3865cf0516a13eede177d7ac')
    # version('0.1.10', commit='212736c1ae3f0429884642a2792853534b36aa52')
    # version('0.1.9',  commit='29890374f2a2560dede9b983547c335bc8e74f96')
    # version('0.1.8',  commit='434d03cfb18036620c8174ccf2d521313061d07a')
    # version('0.1.7',  commit='e2c25ce3985e4dac8c24e7e56cda4c6d87dc49fa')
    # version('0.1.6',  commit='16ad06673d0cc397da04b9a6d22f0d0c3eb26f71')
    # version('0.1.5',  commit='d05e6bb7e30d1ba3f342e4ee1f81d7729651784b')
    # version('0.1.4',  commit='c4df13915a81c9733820d85a5899eb4fe91f4eb0')
    # version('0.1.3',  commit='6484febd58bd8c29d959f1cfe90e0ec89b2f9c25')
    # version('0.1.2',  commit='e46c8f17f31a287c49a4e42cc9700bec56cfcabd')
    # version('0.1.1',  commit='5a4909e39b08b488de471326e97784dc03465e75')
    # version('0.1.0',  commit='5a1c1c6938e7cd01381c1f95ff3f1d9928c8053c')
