# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


# The viewer and trace viewer tar files and sha256sum depend on the
# version and machine type.  Starting with 2019.08, the name of the
# tar file contains the version number.
def viewer_url(ver, mach):
    ver2 = ('-' + ver) if ver >= '2019.08' else ''
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpcviewer{1}-linux.gtk.{2}.tgz'
    ).format(ver, ver2, mach)


def trace_url(ver, mach):
    ver2 = ('-' + ver) if ver >= '2019.08' else ''
    return (
        'http://hpctoolkit.org/download/hpcviewer/{0}/'
        'hpctraceviewer{1}-linux.gtk.{2}.tgz'
    ).format(ver, ver2, mach)


class Hpcviewer(Package):
    """Binary distribution of hpcviewer and hpctraceviewer for the Rice
    HPCToolkit (Linux x86_64, ppc64 and ppc64le).  Note: hpctoolkit
    databases are platform independent, so you don't need to install
    hpctoolkit to run the viewers and it's common to run hpcrun and
    hpcviewer on different machines."""

    homepage = "http://hpctoolkit.org"
    maintainers = ['mwkrentel']

    viewer_sha = {
        ('2019.08', 'x86_64'):  '249aae6a23dca19286ee15909afbeba5e515388f1c1ad87f572454534fccb9f2',
        ('2019.08', 'ppc64'):   'f91b4772c92c05a4a35c88eec094604f3c233c7233adeede97acba38592da379',
        ('2019.08', 'ppc64le'): 'b1bd5c76b37f225a01631193e0a62524bd41a54b3354a658fdfd0f66c444cc28',
        ('2019.07', 'x86_64'):  'e999781d6a7d178cb1db5b549650024fa9b19891e933bac8b0441d24e7bf015c',
        ('2019.07', 'ppc64'):   '057ce0e2d6be5639639f762fb43b116fe31fb855745abaf4ea26bd281cffaab1',
        ('2019.07', 'ppc64le'): '40d6928e0761568168f3ce34f3ed320916ea60bda830dd74513897ef77386b28',
        ('2019.04', 'x86_64'):  'c524498ef235171e298c8142b7e73b0a1f7c433f9c471fb692d31f0685e53aa4',
        ('2019.04', 'ppc64'):   'dc9daee886ba72c0615db909860ee1aed0979f12c0d113efbe721ddabdf55199',
        ('2019.04', 'ppc64le'): 'dddabccef156996d390653639096ad3e27b7384a5754f42084f50c4a50a9009b',
        ('2019.02', 'x86_64'):  'e24368a3ec27b82736a781971a8371abfe7744b2a4f68b7b41d76f84af306b83',
        ('2019.02', 'ppc64'):   '72c1ef1a5682c3273e900bb248f126428a02dfe728af0c49c7ee8381938d1e18',
        ('2019.02', 'ppc64le'): '02aaf27bb5b0f72d5b5738289bce60f6ef0ef7327ca96a890892509a09adc946',
    }

    trace_sha = {
        ('2019.08', 'x86_64'):  '6cefed6a397298ab31cadd10831f5d5533d3f634a4a76bb93f686e603a42c5ed',
        ('2019.08', 'ppc64'):   '64ca5605c89dd3065cacaeee4a8e2ac14b47953530711ed9e04666c8435e44e8',
        ('2019.08', 'ppc64le'): 'bee03b5cb2de7e8556cf1249f98ece7848c13a0de6b8ba71786c430da68f7bcc',
        ('2019.07', 'x86_64'):  '267052cf742d12bbe900bc03bc7c47c8e1704fbaad0e1a3fc77b73dc506d5a68',
        ('2019.07', 'ppc64'):   '5ae63d8e2f2edf5c3b982d3663311e4d55f9b378f512926b3ebadab27ba72e22',
        ('2019.07', 'ppc64le'): 'c2883714cbafa5252432c52d1d32ab5f34554b33a9bad20dcd2c0632388fbee5',
        ('2019.04', 'x86_64'):  'f5f908c0e52c97a72af1af8519f4b191298fe52bd811dd06a051b68cd7bcce27',
        ('2019.04', 'ppc64'):   '221683c992e4fe2cd9079ad2ebb531d99d04a3cbb3a8860f795b276b1eaeab19',
        ('2019.04', 'ppc64le'): 'fe539c6a165a72bba6ea7bdb34a90d862d427c4d55095c97794d54e6dd9d3075',
        ('2019.02', 'x86_64'):  '5ff11317a638318295821204ffcb1276e9da1684cd5f298410ae2bf78ce88b6b',
        ('2019.02', 'ppc64'):   '95b2a7d848ecb924591c248f5e47c641646ef90a071db48237ddb96c4b71a8fb',
        ('2019.02', 'ppc64le'): '01a159306e7810efe07157ec823ac6ca7570ec2014c95db599a3f90eee33355c',
    }

    version_list = ['2019.02', '2019.04', '2019.07', '2019.08']

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
