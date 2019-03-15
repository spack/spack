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
        ('2019.02', 'x86_64'):  'e24368a3ec27b82736a781971a8371abfe7744b2a4f68b7b41d76f84af306b83',
        ('2019.02', 'ppc64'):   '72c1ef1a5682c3273e900bb248f126428a02dfe728af0c49c7ee8381938d1e18',
        ('2019.02', 'ppc64le'): '02aaf27bb5b0f72d5b5738289bce60f6ef0ef7327ca96a890892509a09adc946',
    }

    trace_sha = {
        ('2019.02', 'x86_64'):  '5ff11317a638318295821204ffcb1276e9da1684cd5f298410ae2bf78ce88b6b',
        ('2019.02', 'ppc64'):   '95b2a7d848ecb924591c248f5e47c641646ef90a071db48237ddb96c4b71a8fb',
        ('2019.02', 'ppc64le'): '01a159306e7810efe07157ec823ac6ca7570ec2014c95db599a3f90eee33355c',
    }

    for ver in ['2019.02']:
        key = (ver, platform.machine())
        if key in viewer_sha and key in trace_sha:
            version(ver, url=viewer_url(*key), sha256=viewer_sha[key])

            resource(name='hpctraceviewer', url=trace_url(*key),
                     sha256=trace_sha[key], destination='TRACE')

    depends_on('java@8', type=('build', 'run'))

    # Both hpcviewer and trace viewer have an install script.
    def install(self, spec, prefix):
        args = [
            '--java', spec['java'].home,
            prefix
        ]

        inst = Executable(join_path('.', 'install'))
        inst(*args)

        cd(join_path('TRACE', 'hpctraceviewer'))

        inst = Executable(join_path('.', 'install'))
        inst(*args)
