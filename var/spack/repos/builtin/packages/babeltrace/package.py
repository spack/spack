# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Babeltrace(AutotoolsPackage):
    """Babeltrace is a trace viewer and converter reading and writing the
    Common Trace Format (CTF). Its main use is to pretty-print CTF traces
    into a human-readable text output ordered by time."""

    homepage = "http://www.efficios.com/babeltrace"
    url      = "https://www.efficios.com/files/babeltrace/babeltrace-1.2.4.tar.bz2"

    version('2.0.0', sha256='4511441d98066fdfa00668f1c46036cc81c4582e3802cf861aab5e60960ebfde')
    version('1.5.8', sha256='9ff143e4d1d7f1902b05542ac8f1747fb2d7e0ca31c6fa39ccae5765e11d6fc2')
    version('1.5.7', sha256='215331e025ffd39c665a34231b9429180e48aca78f79fb972d0bf1322d2b807b')
    version('1.5.6', sha256='5308bc217828dd571b3259f482a85533554064d4563906ff3c5774ecf915bbb7')
    version('1.5.5', sha256='409146789b4a6b81f6a275fcad932a030743d444f6de5bd4a34aaf17aa72e8ac')
    version('1.5.4', sha256='9643039923a0abc75a25b3d594cee0017423b57f10d2b625e96ed1e8d4891fc1')
    version('1.5.3', sha256='2249fee5beba657731f5d6a84c5296c6517f544bfbe7571bd1fd7af23726137c')
    version('1.5.2', sha256='696ee46e5750ab57a258663e73915d2901b7cd4fc53b06eb3f7a0d7b1012fa56')
    version('1.5.1', sha256='379e96f1cf867f0a198cf1c315c52ec7d7ad67898402bbe22d1404fc38d19d98')
    version('1.5.0', sha256='354e75d74562f5228ab89e5fa16a3b4dffa95e7230c5086b74ffcf11fef60353')
    version('1.4.4', sha256='c6889323533fc3c3b9c78079362ec44c64ad43b375216fda0ea8912681b73b60')
    version('1.4.3', sha256='3c2709f70a0f257921c5aa68e60eab3f6e56ef8ef51f8810ef3e5b34254f9e43')
    version('1.4.2', sha256='cfdd276cccfee4d5af34fb3213d52fca448cabd58a663ac8ee69c1e872bb8eac')
    version('1.4.1', sha256='d452721190a647b0e8bbed3dbc2d9bd8e9056d2fed34afb6ccea8506ec174bb5')
    version('1.4.0', sha256='9469eeb22617cd12668683b04c27003e5337e9ac66ade914988df3642fc0d0e4')
    version('1.3.3', sha256='b4be9c69cc3633564ccfe11d5311ec84d57acf9e40932f0fcf959b266c3a999d')
    version('1.3.2', sha256='d22d77be79f30fd0769a093b8b5a336ea0d45486ab429358ac5deaced00feb23')
    version('1.3.1', sha256='abbcee3ea046478983b0c7011f33984782d24b3229f3145265317a456acb6db1')
    version('1.3.0', sha256='78f09c9eb5e45b9a842f4f5b56990f8d36cac6db13d3e26801fba0fa7334a523')
    version('1.2.6', sha256='5a72bb17ec033814221c97f12cd44cd64f666231f5b384da6a40d0d4d0344cfd')
    version('1.2.5', sha256='82fca76a2e9e3e947197bdf36a9b342328976c9d1e9f62cadaeb3339ea15bc9a')
    version('1.2.4', sha256='666e3a1ad2dc7d5703059963056e7800f0eab59c8eeb6be2efe4f3acc5209eb1')

    depends_on('glib@2.22:', type=('build', 'link'))
    depends_on('uuid')
    depends_on('popt')
