# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


# The viewer and trace viewer tar files and sha256sum depend on the
# version and machine type.
def viewer_url(ver, mach):
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpcviewer-linux.gtk.{1}.tgz'
    ).format(ver, mach)


def trace_url(ver, mach):
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpctraceviewer-linux.gtk.{1}.tgz'
    ).format(ver, mach)


class Hpcviewer(Package):
    """Binary distribution of hpcviewer and hpctraceviewer for the Rice
    HPCToolkit (Linux x86_64, ppc64 and ppc64le).  Note: hpctoolkit
    databases are platform independent, so you don't need to install
    hpctoolkit to run the viewers and it's common to run hpcrun and
    hpcviewer on different machines."""

    homepage = "http://hpctoolkit.org"

    viewer_sha = {
        ('2019.07', 'x86_64'):  '3bc10354e02c4d4b9dfd2075395b380dda8e9436f5cb4c40e4d50fe4795d7270',
        ('2019.07', 'ppc64'):   '28628890c3297754aed06b6ddcefb4f30a563854f28667288660444cfadde2a4',
        ('2019.07', 'ppc64le'): 'bdc1ee69f938996cc795dcd012f1d0d46e7bd594175aad920d39a0a32590a0f9',
        ('2019.04', 'x86_64'):  'c524498ef235171e298c8142b7e73b0a1f7c433f9c471fb692d31f0685e53aa4',
        ('2019.04', 'ppc64'):   'dc9daee886ba72c0615db909860ee1aed0979f12c0d113efbe721ddabdf55199',
        ('2019.04', 'ppc64le'): 'dddabccef156996d390653639096ad3e27b7384a5754f42084f50c4a50a9009b',
        ('2019.02', 'x86_64'):  'e24368a3ec27b82736a781971a8371abfe7744b2a4f68b7b41d76f84af306b83',
        ('2019.02', 'ppc64'):   '72c1ef1a5682c3273e900bb248f126428a02dfe728af0c49c7ee8381938d1e18',
        ('2019.02', 'ppc64le'): '02aaf27bb5b0f72d5b5738289bce60f6ef0ef7327ca96a890892509a09adc946',
    }

    trace_sha = {
        ('2019.07', 'x86_64'):  'c69db0dd10bc861eb7c594cb1e5f32bf9e104d0858c4a3c075b58a446485f2bf',
        ('2019.07', 'ppc64'):   '927c8a2443d4cec3725dab28879f7f1efbc337cdc3c0bb7536ec891daacb50ab',
        ('2019.07', 'ppc64le'): '3b04244e254d9d11802321199c11c8799040f86389b520842af64fa73dfc58a8',
        ('2019.04', 'x86_64'):  'f5f908c0e52c97a72af1af8519f4b191298fe52bd811dd06a051b68cd7bcce27',
        ('2019.04', 'ppc64'):   '221683c992e4fe2cd9079ad2ebb531d99d04a3cbb3a8860f795b276b1eaeab19',
        ('2019.04', 'ppc64le'): 'fe539c6a165a72bba6ea7bdb34a90d862d427c4d55095c97794d54e6dd9d3075',
        ('2019.02', 'x86_64'):  '5ff11317a638318295821204ffcb1276e9da1684cd5f298410ae2bf78ce88b6b',
        ('2019.02', 'ppc64'):   '95b2a7d848ecb924591c248f5e47c641646ef90a071db48237ddb96c4b71a8fb',
        ('2019.02', 'ppc64le'): '01a159306e7810efe07157ec823ac6ca7570ec2014c95db599a3f90eee33355c',
    }

    version_list = ['2019.07', '2019.04', '2019.02']

    for ver in version_list:
        key = (ver, platform.machine())
        if key in viewer_sha and key in trace_sha:
            version(ver, url=viewer_url(*key), sha256=viewer_sha[key])

            resource(name='hpctraceviewer', url=trace_url(*key),
                     sha256=trace_sha[key], placement='TRACE',
                     when='@{0}'.format(ver))

    depends_on('java@8', type=('build', 'run'))

    # Both hpcviewer and trace viewer have an install script.
    def install(self, spec, prefix):
        args = [
            '--java', spec['java'].home,
            prefix
        ]

        inst = Executable(join_path('.', 'install'))
        inst(*args)

        cd('TRACE')

        inst = Executable(join_path('.', 'install'))
        inst(*args)
